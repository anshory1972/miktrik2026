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
   type to **Public**, and choose a username. This
   course uses `miktrik_unpad`, so the link is `https://t.me/miktrik_unpad`.

2. **Create and link the discussion group.** Open the channel, tap its name,
   then **Edit → Discussion → Create a New Group**. Name it and confirm.
   Telegram makes the group and links it in the same action.

3. **Make that group public.** Open the group, tap its name, then
   **Edit → Group Type → Public**, and give it a username. This is not
   optional. See the two rules below.

4. **Post one message per thread.** For every entry in `threads`, post one message in the
   channel announcing that topic. Open the post, copy its link, and note the
   number at the end:

   ```
   https://t.me/miktrik_unpad/6   ->   post 6
   ```

5. **Let the script wire it up.** Do not edit `config.js` by hand. Run:

   ```bash
   python tools/setup_forum.py --channel miktrik_unpad --check
   ```

   That verifies the channel is public and that each post's thread is readable
   from outside, logged out. When it passes, drop `--check` and add the threads:

   ```bash
   python tools/setup_forum.py --channel miktrik_unpad \
       --thread umum=6 --thread lpm-logit-probit=7 \
       --group-link https://t.me/miktrik_unpad_diskusi

   git add -A && git commit -m "Activate forum threads" && git push
   ```

   The script uses only public `t.me` pages. No bot token, no API key, no login.
   It writes nothing when any check fails, so a half-finished Telegram setup
   cannot produce a half-broken site.

Until a thread has a post number, its page shows a plain "not opened yet"
notice rather than a broken widget. Nothing breaks while you are half set up.

### Two rules that cost us an hour, and are in no documentation

Both were found by testing against the live channel, not by reading docs.

**The discussion group must be public.** While the group was private, the
Telegram app showed a Comments button to the admin, but the public web embed
answered `Discussion is not available at the moment.` A logged-out visitor
could see nothing. Making the group public fixed it.

**A post only ever gets the thread state it was born with.** Posts published
before the group was linked, or while it was still private, never acquire a
comment thread afterwards. They stay dead. Finish both steps above *first*,
then publish the posts you intend to use as threads. On this channel, posts 1
to 5 were lost to this and had to be replaced by 6 and 7.

How to read the states from outside:

| What `t.me/<ch>/<n>?embed=1&discussion=1` says | Meaning |
|---|---|
| `Discussion is not available at the moment.` | Broken. No group linked, or the group is private. |
| `Be the first to add a comment` | Working, thread is empty. |
| Rendered comments | Working, thread has content. |

---

## Publishing

Already done. The repository is `anshory1972/miktrik2026` and the site is live at

**https://anshory1972.github.io/miktrik2026/**

Pages is set to deploy from `main` at the repository root. Every `git push` to
`main` republishes within a minute or so. The canonical link tags in each page
are set to the real addresses, which is how Telegram matches a shared link back
to the right page.

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
