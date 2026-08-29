"""The long-form prose for the privacy policy and the terms.

Kept out of landing.py because it is text, not layout, and it changes on a
different clock from the page around it. generate.py wraps it in the same
chrome as everything else.
"""

PRIVACY_H1 = 'Privacy Policy'
PRIVACY_DESC = 'How GoForay, Co. collects, uses, and protects the information engineers and companies give us.'
PRIVACY_BODY = r"""<p class="meta lbl">Effective 27 August 2026 &middot; Last updated 27 August 2026</p>

<p>Foray is an engineering search firm. Engineers tell us what they want next and we
  bring them roles; companies tell us what they are hiring for and we bring them
  engineers. This policy explains what we collect while doing that, why, who else
  sees it, and what you can ask us to do about it.</p>

<p>It covers this website, the forms on it, our phone line, our text conversations,
  and the candidate portal.</p>

<h2>Who we are</h2>
<p>Foray is operated by <strong>GoForay, Co.</strong>, a Delaware corporation, with a
  registered office at 131 Continental Drive, Suite 305, Newark, Delaware 19713.
  Reach us at <a href="mailto:anna@goforay.io">anna@goforay.io</a>.</p>

<h2>What we collect</h2>

<h3>If you are an engineer</h3>
<p>When you join the pool, the form asks for your name, email, LinkedIn, GitHub, and
  a short note on what you want next. Optionally: a piece of work you are proud of,
  years of experience, timeline, location and remote preference, and your work
  authorization. If we go on to work with you, we also hold your r&eacute;sum&eacute;, the roles
  we put you forward for, and the messages we exchange.</p>

<h3>If you are hiring</h3>
<p>Your name, company, email, the role you are filling, the job posting link, and the
  job description.</p>

<h3>Calls</h3>
<p>Our intake assistant is an AI. It says so at the start of every call, and it asks
  your permission to record before it asks anything else. If you say no, we do not record and we do not continue; a person follows up instead. Permission is
  asked <strong>per call</strong>, not once and assumed forever. Where we record, we
  keep the recording and a written transcript.</p>

<h3>Texts</h3>
<p>The messages you exchange with us, any files you send in a thread, and the record
  of how and when you agreed to be texted.</p>

<h3>Connected apps, only if you choose to connect one</h3>
<p>You can connect Gmail, Outlook, or GitHub so we can find your r&eacute;sum&eacute; instead of
  making you dig it out. If you do:</p>
<ul>
  <li>We request read-only access and nothing wider: Gmail <code>gmail.readonly</code>,
    Microsoft <code>Mail.Read</code>, GitHub <code>read:user</code>. We never request
    permission to send mail as you.</li>
  <li>We run a fixed set of searches looking for r&eacute;sum&eacute; attachments. We do not read
    your email for content and we do not index your mailbox.</li>
  <li>What we keep is the r&eacute;sum&eacute; file and basic profile facts. Subject lines, bodies,
    and snippets are not stored: there is no field in our system that holds them.</li>
  <li>Tokens are encrypted at rest. We read once when you connect, and again only if
    you ask us to re-check. There is no background sync.</li>
  <li>Disconnect any time. We delete our copy of the token and revoke it upstream where the provider allows it. Google and GitHub do; Microsoft does not, so we delete
    our copy and you can revoke it from your Microsoft account.</li>
</ul>

<h3>Automatically</h3>
<p>When you submit a form we store your browser's user agent, the page that referred
  you, and a salted hash of your IP address. The hash is used to rate-limit submissions and nothing else. We do not keep the IP itself. This site does not
  use advertising or cross-site tracking cookies. We use privacy-preserving analytics
  to count page views in aggregate.</p>

<h2>What we do not ask for</h2>
<div class="note">
  <p><strong>Salary history.</strong> We ask what you are targeting going forward. We
    never ask what you make now or made before, and if you mention it we do not record
    it or use it to steer anything.</p>
  <p><strong>Protected characteristics.</strong> We never ask about your age, race,
    religion, health, disability, family or marital status, or pregnancy. If you
    volunteer something in one of these categories, our assistant acknowledges it and moves on. There is no field for it to land in.</p>
</div>

<h2>How we use it</h2>
<ul>
  <li>To match engineers to open roles, and roles to engineers.</li>
  <li>To prepare and submit applications where you have asked us to.</li>
  <li>To tell you where things stand and to answer your questions.</li>
  <li>To introduce you to a company, once you have told us that is okay.</li>
  <li>To keep a record of the permissions you gave us and when.</li>
  <li>To operate, secure, and improve the service, and to meet our legal obligations.</li>
</ul>
<p>We do not use your information to train third-party AI models, and we do not use it
  for advertising.</p>

<h2>Text messaging</h2>
<p>We text you only if you asked us to. There are two ways that happens: you tell us
  yes on a recorded call when we ask, verbatim, &ldquo;Can I text you updates at this number?&rdquo; or you text our number first. Only a clear yes counts; we do
  not re-ask or rephrase to get a better answer. The forms on this site do not collect
  a phone number and are not a way to opt in to texts.</p>
<p>Our first message identifies us and asks you to reply so we know we have the right
  number. Nothing else goes out until you do. After that, our messages are about your
  own search: application status, roles that match what you told us, requests for a
  missing detail, and replies to what you send us. They are not marketing.</p>
<div class="note">
  <p><strong>No mobile information will be shared with third parties or affiliates for
    marketing or promotional purposes. All other categories of data sharing described
    in this policy exclude text messaging originator opt-in data and consent; that
    information is not shared with any third party.</strong></p>
</div>
<p>Reply <strong>STOP</strong> at any time and we stop texting you. Reply
  <strong>HELP</strong> for help. Message frequency varies with your own search.
  Message and data rates may apply.</p>
<p>Our voice and text line is <strong>coming soon</strong>. We will publish the number
  here once it is live.</p>

<h2>Who we share it with</h2>

<h3>Companies hiring</h3>
<p>The point of the service is getting your profile in front of a company that is
  hiring, and we ask you before we do it. When we submit an application on your behalf,
  the company receives what any applicant would send: your r&eacute;sum&eacute;, your cover letter,
  and your answers to their questions. Anything you tell us you would rather we did not
  repeat to a company, we do not.</p>

<h3>Service providers</h3>
<p>They process your data on our instructions and for no purpose of their own.</p>
<div class="tablewrap">
  <table>
    <tr><th>Provider</th><th>What they handle</th></tr>
    <tr><td>Vercel</td><td>Website hosting and form submissions</td></tr>
    <tr><td>Twilio</td><td>Our phone number, calls, and text messages</td></tr>
    <tr><td>Retell AI</td><td>The voice assistant: call audio and transcripts</td></tr>
    <tr><td>Linq</td><td>Message delivery on our text channel</td></tr>
    <tr><td>Anthropic</td><td>The AI models behind the assistant</td></tr>
  </table>
</div>

<h3>Legal</h3>
<p>We disclose information where the law requires it, to respond to lawful requests, to
  enforce our terms, or to protect the rights and safety of people using the service.
  If we are ever part of a merger, acquisition, or sale of assets, your information may
  transfer with it, and this policy travels with it.</p>

<h3>What we do not do</h3>
<p>We do not sell your personal information, and we do not share it for cross-context
  behavioral advertising. We have not done so in the preceding twelve months. We do not
  buy, rent, or trade phone numbers, and every number we text belongs to someone who
  asked us to.</p>

<h2>How long we keep it</h2>
<p>We keep your profile, your submissions, and our message history for as long as you
  are working with us and for a reasonable period afterwards, so a returning engineer
  does not start from nothing. Records of the permissions you gave us, including a text opt-in and the exact wording you heard, are kept for as long as we may
  need to show consent was given. Ask us to delete your information and we will,
  subject to records we are required to keep.</p>

<h2>Your choices and rights</h2>
<ul>
  <li><strong>Stop the texts</strong>: reply STOP, any time.</li>
  <li><strong>Disconnect an app</strong>: from the connect page, any time.</li>
  <li><strong>Stop us sharing with companies</strong>: tell us, and we stop.</li>
  <li><strong>See what we hold, correct it, or delete it</strong>: email
    <a href="mailto:anna@goforay.io">anna@goforay.io</a>.</li>
</ul>
<p>If you are a California resident, the CCPA and CPRA give you the right to know what
  we collect and why, to delete it, to correct it, to opt out of sale or sharing (we do
  neither), and not to be treated differently for exercising any of these. We verify
  identity before acting on a request and respond within the time the law allows. You
  may use an authorized agent.</p>
<p>Under California law, candidates are entitled to the pay scale for a role on request.
  Ask us and we will get it for you.</p>

<h2>Automated decisions</h2>
<p>Our assistants collect information and prepare applications. They do not decide whether you get hired. Companies do. Where we rank roles, we rank them against
  the preferences <strong>you</strong> gave us. If you would rather a person looked at
  your file instead of the assistant, ask and we will arrange it.</p>

<h2>Security</h2>
<p>Access to your data is limited to the people who need it. Connected-app tokens are
  encrypted at rest, traffic to our servers is encrypted in transit, and IP addresses
  are hashed rather than stored. No system is perfectly secure and we will not pretend otherwise, but if a breach affects you, we will tell you as the law requires.</p>

<h2>Minors</h2>
<p>Foray is for adults. We do not knowingly collect information from anyone under 18.
  If our assistant realizes it is talking to a minor, it stops and hands off to a
  person. If you believe a minor has given us information, email us and we will delete
  it.</p>

<h2>Changes</h2>
<p>We will update this policy as the service changes. The effective date at the top
  tells you which version you are reading, and we keep a record of the wording that was
  in place when you gave us each permission, so a change here never rewrites what
  you originally agreed to.</p>

<h2>Contact</h2>
<p>Questions, requests, or complaints:
  <a href="mailto:anna@goforay.io">anna@goforay.io</a>, or write to GoForay, Co.,
  131 Continental Drive, Suite 305, Newark, Delaware 19713.</p>"""

TERMS_H1 = 'Terms of Service'
TERMS_DESC = 'The terms you agree to when you use Foray, operated by GoForay, Co.'
TERMS_BODY = r"""<p class="meta lbl">Effective 27 August 2026 &middot; Last updated 27 August 2026</p>

<p>These terms are the agreement between you and <strong>GoForay, Co.</strong>, a
  Delaware corporation doing business as Foray (&ldquo;Foray,&rdquo; &ldquo;we,&rdquo;
  &ldquo;us&rdquo;), covering your use of this website, our forms, our phone line, our
  text conversations, and the candidate portal. Using Foray means you accept them. If
  you do not, please do not use the service.</p>
<p>How we handle your information is covered separately in our
  <a href="privacy.html">Privacy Policy</a>, which forms part of these terms.</p>

<h2>1. What Foray does</h2>
<p>Foray is an engineering search firm. For engineers: we take your details, match you
  to open roles, prepare applications, submit them where you ask us to, and keep you
  updated. For companies: we run a search against the role you give us and put
  candidates in front of you. Some of that work is done by AI assistants, on the phone
  and over text.</p>
<div class="note">
  <p><strong>You are talking to an AI.</strong> Our intake and messaging assistants say
    so up front and will tell you plainly if you ask. They can be wrong. Nothing an
    assistant says is a promise of a role, an interview, or an introduction, and nothing
    it says is legal, immigration, tax, or financial advice.</p>
</div>

<h2>2. Who can use it</h2>
<p>You must be at least 18 and legally able to enter a contract. Foray is currently
  offered in the United States. You are responsible for confirming you have the right
  to work where you apply.</p>

<h2>3. What you authorize us to do</h2>
<p>If you join the pool as an engineer, you are asking us to, and authorizing us to:</p>
<ul>
  <li>Use what you tell us to look for roles matching your stated preferences.</li>
  <li>Prepare application materials for you (a r&eacute;sum&eacute;, a cover letter, and answers to a company's questions) drafted from what you told us.</li>
  <li>Submit applications on your behalf to roles you have approved, and create accounts
    on company application sites where that is the only way to apply.</li>
  <li>Correspond with companies about your application, using an email address on our
    domain that forwards to your file.</li>
  <li>Put your profile in front of companies we are searching for, but only once you have told us that is okay.</li>
</ul>
<p>You can tell us to stop any of this at any time, and we will.</p>

<h2>4. What we need from you</h2>
<ul>
  <li>Tell us the truth. Everything we put in front of a company comes from what you
    told us, and you are responsible for it being accurate.</li>
  <li>Only send us material you have the right to send: your own r&eacute;sum&eacute; and
    work history, not a former employer's confidential information.</li>
  <li>Keep your contact details current, so we can reach you.</li>
  <li>Do not use Foray to harass anyone, to misrepresent who you are, to break the law,
    or to attack or probe our systems.</li>
</ul>

<h2>5. If you are hiring</h2>
<p>Candidate information we share with you is confidential and given for one purpose:
  evaluating that person for the role you told us about. Do not forward it, add it to a
  database, or use it for another search. Our fees, guarantee, and payment terms are set
  out in the separate search agreement we sign with you; these terms do not replace it.
  Hiring decisions are yours, and you are responsible for making them lawfully.</p>

<h2>6. Text messages</h2>
<p>We text you only if you asked us to, either by telling us yes on a recorded
  call, or by texting us first. The forms on this site do not collect a phone number and
  are not a way to opt in. Our messages are about your own search: application status,
  roles matching what you told us, requests for a missing detail, and replies to what
  you send us. They are not marketing.</p>
<p>Reply <strong>STOP</strong> at any time and we stop. Reply <strong>HELP</strong> for
  help. Message frequency varies with your own search. Message and data rates may apply.
  Carriers are not liable for delayed or undelivered messages.</p>
<p>Our voice and text line is <strong>coming soon</strong>. We will publish the number
  here once it is live.</p>

<h2>7. Fees</h2>
<p>Foray is free for engineers. If that ever changes we will tell you before any charge
  applies and you will have to agree to it first. We are paid by the companies we search
  for, not by candidates.</p>

<h2>8. No guarantee of a job</h2>
<p>We do not control hiring decisions and we do not promise results. Using Foray does
  not guarantee that you will be matched to a role, that an application will be
  submitted, that a company will respond, that you will get an interview, or that you
  will be hired. Companies make their own decisions on their own criteria.</p>

<h2>9. Your content</h2>
<p>Your r&eacute;sum&eacute; and everything else you give us stays yours. You grant us the
  permission we need to use it for the purpose you gave it to us for (matching, preparing applications, and submitting them on your behalf) and nothing beyond that. Ask us to delete it and we will, subject to records we have to keep, which the
  <a href="privacy.html">Privacy Policy</a> describes.</p>
<p>The service itself (our software, brand, and content) belongs to us.
  You may use it, but you may not copy it, resell it, reverse-engineer it, or scrape it.</p>

<h2>10. Third-party services</h2>
<p>Foray connects to services we do not control: company application sites, job boards,
  and apps you choose to connect. We are not responsible for what they do, for their
  terms, or for their availability. Connecting an app is optional and you can disconnect
  it at any time.</p>

<h2>11. Availability</h2>
<p>We may change, suspend, or discontinue any part of the service, and will give notice
  where it is reasonable to do so.</p>

<h2>12. Disclaimers and limits</h2>
<p>To the fullest extent the law allows, the service is provided &ldquo;as is&rdquo; and
  &ldquo;as available,&rdquo; without warranties of any kind, express or implied,
  including merchantability, fitness for a particular purpose, and non-infringement.</p>
<p>To the fullest extent the law allows, we are not liable for indirect, incidental,
  special, consequential, or punitive damages, or for lost opportunities, lost earnings,
  or lost data. Our total liability for any claim relating to the service will not
  exceed one hundred US dollars (USD 100) or the amount you paid us in the twelve months
  before the claim, whichever is greater. Some jurisdictions do not allow these limits,
  in which case they apply to the extent permitted.</p>

<h2>13. Ending it</h2>
<p>You can stop using Foray at any time and ask us to close your file. We may suspend or
  end your access if you breach these terms or if we stop offering the service. The
  sections that by their nature should survive (content ownership, disclaimers, limits, and governing law) survive.</p>

<h2>14. Governing law</h2>
<p>These terms are governed by the laws of the State of Delaware, without regard to its
  conflict-of-laws rules. Any dispute will be brought in the state or federal courts
  located in Delaware, and we each consent to that jurisdiction. Nothing here waives any
  right you cannot waive under the law where you live.</p>

<h2>15. Changes</h2>
<p>We may update these terms. The effective date at the top tells you which version you
  are reading. If a change is material we will give notice before it takes effect, and
  continuing to use Foray afterwards means you accept it.</p>

<h2>16. Contact</h2>
<p><a href="mailto:anna@goforay.io">anna@goforay.io</a>, or write to GoForay, Co.,
  131 Continental Drive, Suite 305, Newark, Delaware 19713.</p>"""
