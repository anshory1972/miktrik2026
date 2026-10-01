# Working rules for this repository

## Never report a publish you have not fetched back

This repository is published as a **GitHub Pages site** at
`https://anshory1972.github.io/miktrik2026/`, and the PMT assignment page has a
second copy on `https://sdgcenter.unpad.ac.id/aay/miktrik/pmtprobit.html`, which
sits **behind Cloudflare**.

"Updated", "live", "published", "deployed", "done" — these are claims about what
a student can now see. Write them only after fetching the public URL and
comparing it with what was sent:

```bash
curl -s  https://anshory1972.github.io/miktrik2026/topics/02-pmt-assignment.html | grep -o 'pmt-hero[^"]*'
curl -sI https://anshory1972.github.io/miktrik2026/assets/art/<file>
curl -s  https://anshory1972.github.io/miktrik2026/assets/art/<file> | sha256sum   # match the local file
```

None of these is evidence of publication: a clean `git push`, a successful
`scp`, an `ls` on the origin server showing the new bytes, a 200 on the old URL.

- **GitHub Pages** rebuilds in roughly 10–60 s and answers 404 or the previous
  content until it does. Poll until it matches; do not announce on the push.
- **Cloudflare** serves a replaced file from cache under an unchanged name —
  `cf-cache-status: HIT` with the old `content-length` — long after the origin
  is right. Give a replaced static asset a **new URL**: the page builders in
  `E:\pmtwb\synthetic_mc\assignment\` publish `pmt-hero-<sha8>.jpg` and delete
  the previous hash for exactly this reason.

If a check has not been run, say which one is missing. Do not round a partial
check up to "done".
