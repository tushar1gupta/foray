-- Reference copy. api/submit.js applies this itself on first call,
-- so you only need this if you prefer to manage schema by hand.

CREATE TABLE IF NOT EXISTS submissions (
  id          bigserial PRIMARY KEY,
  kind        text NOT NULL CHECK (kind IN ('company','engineer')),
  created_at  timestamptz NOT NULL DEFAULT now(),
  name        text NOT NULL,
  email       text NOT NULL,
  payload     jsonb NOT NULL,   -- every submitted field, keyed by its data-label
  user_agent  text,
  referer     text,
  ip_hash     text              -- salted sha256, for rate limiting only
);

CREATE INDEX IF NOT EXISTS submissions_created_idx ON submissions (created_at DESC);
CREATE INDEX IF NOT EXISTS submissions_kind_idx    ON submissions (kind, created_at DESC);
CREATE INDEX IF NOT EXISTS submissions_rate_idx    ON submissions (ip_hash, created_at DESC);

-- Recent companies:
--   SELECT created_at, name, email, payload->>'Company', payload->>'Role'
--   FROM submissions WHERE kind='company' ORDER BY created_at DESC LIMIT 50;
