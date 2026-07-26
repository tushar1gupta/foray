const crypto = require('crypto');
const { Pool } = require('pg');

// attachDatabasePool releases idle clients before the function suspends under
// Fluid Compute. Without it, pooled connections leak across invocations.
let attachDatabasePool;
try { attachDatabasePool = require('@vercel/functions').attachDatabasePool; } catch (_) {}

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 3,
  idleTimeoutMillis: 10000,
  connectionTimeoutMillis: 8000,
});
if (attachDatabasePool) attachDatabasePool(pool);

/* Required labels mirror the data-req attributes in the markup. Keep in sync. */
const FORMS = {
  company: {
    required: ['Name', 'Company', 'Email', 'Job posting link', 'Job description'],
    subject: f => 'New search: ' + (f.Company || 'unknown') + (f.Role ? ' - ' + f.Role : ''),
  },
  engineer: {
    required: ['Name', 'Email', 'LinkedIn', 'GitHub', 'What they want next'],
    subject: f => 'Engineer intake: ' + (f.Name || 'unknown'),
  },
};

const CAPS = { 'Job description': 20000, 'What they want next': 8000, Email: 320, Name: 200 };
const CAP_DEFAULT = 2000;
const MAX_BODY = 96 * 1024;
const MAX_FIELDS = 40;
const RATE_MAX = 5;
const RATE_WINDOW = '15 minutes';
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

let schemaReady;
function ensureSchema() {
  if (!schemaReady) {
    schemaReady = pool.query(`
      CREATE TABLE IF NOT EXISTS submissions (
        id          bigserial PRIMARY KEY,
        kind        text NOT NULL CHECK (kind IN ('company','engineer')),
        created_at  timestamptz NOT NULL DEFAULT now(),
        name        text NOT NULL,
        email       text NOT NULL,
        payload     jsonb NOT NULL,
        user_agent  text,
        referer     text,
        ip_hash     text
      );
      CREATE INDEX IF NOT EXISTS submissions_created_idx ON submissions (created_at DESC);
      CREATE INDEX IF NOT EXISTS submissions_kind_idx    ON submissions (kind, created_at DESC);
      CREATE INDEX IF NOT EXISTS submissions_rate_idx    ON submissions (ip_hash, created_at DESC);
    `).catch(err => { schemaReady = null; throw err; });
  }
  return schemaReady;
}

function clientIp(req) {
  const xff = req.headers['x-forwarded-for'];
  if (typeof xff === 'string' && xff) return xff.split(',')[0].trim();
  return req.headers['x-real-ip'] || (req.socket && req.socket.remoteAddress) || '';
}

/* Salted hash, so we can rate limit without retaining raw IP addresses. */
function hashIp(ip) {
  if (!ip) return null;
  return crypto.createHash('sha256')
    .update((process.env.IP_SALT || 'foray') + '|' + ip)
    .digest('hex').slice(0, 32);
}

function validate(kind, fields) {
  const spec = FORMS[kind];
  if (!spec) return { error: 'Unknown form.' };

  const keys = Object.keys(fields);
  if (keys.length > MAX_FIELDS) return { error: 'Too many fields.' };

  const clean = {};
  for (const k of keys) {
    if (typeof k !== 'string' || k.length > 60) return { error: 'Bad field name.' };
    const raw = fields[k];
    if (raw == null) continue;
    if (typeof raw !== 'string') return { error: 'Bad field value.' };
    const v = raw.trim();
    if (!v) continue;
    if (v.length > (CAPS[k] || CAP_DEFAULT)) {
      return { error: '"' + k + '" is too long.' };
    }
    clean[k] = v;
  }

  const missing = spec.required.filter(r => !clean[r]);
  if (missing.length) return { error: 'Missing required fields.', missing };
  if (!EMAIL_RE.test(clean.Email)) return { error: 'That email address looks wrong.' };

  return { clean, subject: spec.subject(clean) };
}

async function notify(kind, subject, clean, id) {
  const key = process.env.RESEND_API_KEY;
  const to = process.env.NOTIFY_TO;
  const from = process.env.NOTIFY_FROM;
  if (!key || !to || !from) return { skipped: 'email env vars not set' };

  const lines = Object.keys(clean).map(k => k + ': ' + clean[k]);
  const text = lines.join('\n') + '\n\n--\nform: ' + kind + '\nsubmission id: ' + id + '\n';

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from, to, reply_to: clean.Email, subject, text }),
  });
  if (!res.ok) throw new Error('resend ' + res.status + ' ' + (await res.text()).slice(0, 300));
  return { sent: true };
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'Method not allowed.' });
  }

  const len = Number(req.headers['content-length'] || 0);
  if (len > MAX_BODY) return res.status(413).json({ ok: false, error: 'Submission too large.' });

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (_) {
      return res.status(400).json({ ok: false, error: 'Malformed request.' });
    }
  }
  if (!body || typeof body !== 'object') {
    return res.status(400).json({ ok: false, error: 'Malformed request.' });
  }
  // Bots that POST directly tend to fill every input they can find.
  if (body.confirm_url) return res.status(200).json({ ok: true });

  const v = validate(body.kind, body.fields || {});
  if (v.error) {
    return res.status(400).json({ ok: false, error: v.error, missing: v.missing || [] });
  }

  const ipHash = hashIp(clientIp(req));

  try {
    await ensureSchema();

    if (ipHash) {
      const { rows } = await pool.query(
        'SELECT count(*)::int AS n FROM submissions ' +
        "WHERE ip_hash = $1 AND created_at > now() - interval '" + RATE_WINDOW + "'",
        [ipHash]
      );
      if (rows[0].n >= RATE_MAX) {
        return res.status(429).json({
          ok: false,
          error: 'Too many submissions just now. Email contact@goforay.io instead.',
        });
      }
    }

    const { rows } = await pool.query(
      `INSERT INTO submissions (kind, name, email, payload, user_agent, referer, ip_hash)
       VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING id`,
      [
        body.kind,
        v.clean.Name,
        v.clean.Email,
        JSON.stringify(v.clean),
        String(req.headers['user-agent'] || '').slice(0, 500),
        String(req.headers.referer || '').slice(0, 500),
        ipHash,
      ]
    );
    const id = rows[0].id;

    // Stored is the source of truth. A failed notification must not fail the request.
    try {
      const out = await notify(body.kind, v.subject, v.clean, id);
      if (out.skipped) console.warn('submission', id, 'saved, notification skipped:', out.skipped);
    } catch (err) {
      console.error('submission', id, 'saved but notification failed:', err.message);
    }

    return res.status(201).json({ ok: true, id: String(id) });
  } catch (err) {
    console.error('submission failed:', err);
    return res.status(500).json({
      ok: false,
      error: 'Something broke on our end. Email contact@goforay.io and we will pick it up.',
    });
  }
};
