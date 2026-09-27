# Mikroekonometrika 2026

Course site for microeconometrics: materials plus an open discussion forum.

Static HTML served by GitHub Pages. No build step, no framework, no server.
Discussion runs on Telegram and is embedded into the pages, so **reading needs
no account** and only **asking** needs Telegram.

---

## How the forum works

Telegram publishes an official *discussion widget*. A script tag carrying
`data-telegram-discussion="<channel>/<post>"` replaces itself with an iframe
showing the comment thread under that channel post. Because a public channel is
publicly readable, visitors see every question and answer without logging in.

That means the unit is **not a group on its own**. You need two objects:

| Object | Role |
|---|---|
| A **public channel** | You post one message per discussion topic. This is what the web page embeds. |
| A **discussion group** linked to it | Comments on each channel post land here. Students post from Telegram. |

The page is a *live view* of Telegram, not a copy. Delete a message in Telegram
and it disappears from the website too, so moderation needs no second step.

---

## One-time setup in Telegram

Do these in the Telegram app. It takes about five minutes.

1. **Create the channel.** New Message → New Channel. Give it a name, set the
   type to **Public**, and choose a username, for example `miktrik2026`. The
   link becomes `https://t.me/miktrik2026`.

2. **Create the discussion group.** New Message → New Group. Call it something
   like *Mikroekonometrika 2026 — Diskusi*. You can leave it empty.

3. **Link them.** Open the channel → Manage Channel → **Discussion** → pick the
   group you just made. A *Comments* button now appears under every channel post.

4. **Tell the site about the channel.** Open `assets/config.js` and set:

   ```js
   channel: "miktrik2026",          // no "@"
   groupLink: "https://t.me/...",   // the group's invite link, optional
   ```

5. **Open each thread.** For every entry in `threads`, post one message in the
   channel announcing that topic. Open the post, copy its link, and take the
   number at the end:

   ```
   https://t.me/miktrik2026/7   ->   post: 7
   ```

   Put that number into the matching thread in `assets/config.js`.

Until a thread has a `post` number, its page shows a plain "not opened yet"
notice rather than a broken widget. Nothing breaks while you are half set up.

---

## Publishing to GitHub Pages

```bash
git remote add origin https://github.com/anshory1972/miktrik2026.git
git push -u origin main
```

Then in the repository: **Settings → Pages → Source: Deploy from a branch →
`main` / `(root)`**. The site appears at
`https://anshory1972.github.io/miktrik2026/`.

Once you know that URL, uncomment the `<link rel="canonical">` line in each HTML
file and set it to the real address. Telegram uses it to match a shared link
back to the right page.

The `.nojekyll` file is required. Without it GitHub runs Jekyll, which ignores
files and folders beginning with an underscore.

---

## Repository layout

```
index.html                     course home, list of materials
forum.html                     all discussion threads on one page
topics/                        one page per topic
  _template.html               copy this to start a new topic
  01-lpm-logit-probit.html
assets/
  config.js                    THE ONLY FILE YOU EDIT TO RUN THE FORUM
  forum.js                     widget logic, leave alone
  style.css                    house style, shared by every page
materials/
  slides/                      lecture PDFs
  stata/                       do-files
  data/                        datasets
```

### Adding a topic

1. Copy `topics/_template.html` to `topics/NN-slug.html`.
2. Fill in the title, the prose, and the download rows.
3. Add a thread with a matching `slug` to `assets/config.js`.
4. Add a card for it in `index.html`.

---

## Rules worth stating to students on day one

- Everything written in the forum is **public on the website**, including the
  student's Telegram display name.
- Grades and anything personal go by email, never in the forum.
- A public channel's discussion group can be joined by anyone, so use slow mode
  and remove strangers if spam appears.

---

## Limits to respect

| Limit | Value |
|---|---|
| Published GitHub Pages site, total | 1 GB |
| Single file GitHub will accept | 100 MB |

Current `materials/` size is about 10 MB. If a dataset ever approaches the file
cap, link to it rather than committing it.

---

## Verifying a change

Layout faults in these pages are almost always horizontal overflow or a CSS
specificity clash. Both are cheap to test. Render each page in headless Chrome
inside an iframe of an exact phone width and assert `scrollWidth == clientWidth`,
then look at the screenshot. Headless Chrome will not lay out below about 485px,
so the iframe is the only honest way to measure 360 and 390.

One trap already bit this stylesheet and is documented in `assets/style.css`:
`.prose a` is specificity (0,1,1) and beats a bare `.btn` at (0,1,0), which
painted a button label terracotta on a terracotta ground. Button rules repeat
the `a` element for that reason.
