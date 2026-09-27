/* ==========================================================================
   THE ONLY FILE YOU NEED TO EDIT TO RUN THE FORUM.
   Everything else reads from here. See README.md for the Telegram setup.
   ========================================================================== */

window.FORUM_CONFIG = {

  /* -----------------------------------------------------------------------
     1. Your PUBLIC Telegram channel username, WITHOUT the "@".
        Leave it as "" and every page shows a "not configured yet" notice
        instead of a broken widget.
        Example: if the channel is https://t.me/miktrik2026 write "miktrik2026"
     ----------------------------------------------------------------------- */
  channel: "",

  /* -----------------------------------------------------------------------
     2. The discussion group people are sent to when they want to post.
        Usually the invite link of the group linked to the channel.
        Leave "" to fall back to the channel link.
     ----------------------------------------------------------------------- */
  groupLink: "",

  /* -----------------------------------------------------------------------
     3. One entry per discussion thread.
        "post" is the channel post number. Open the post in Telegram, copy
        the link, and take the number after the channel name:
            https://t.me/miktrik2026/7   ->   post: 7
        "slug" is what a topic page uses to ask for its own thread.
     ----------------------------------------------------------------------- */
  threads: [
    {
      slug: "umum",
      post: null,
      title: "Tanya apa saja",
      note: "Pertanyaan umum tentang kuliah, jadwal, tugas, dan Stata."
    },
    {
      slug: "lpm-logit-probit",
      post: null,
      title: "LPM, Logit, dan Probit",
      note: "Diskusi untuk materi pertama, termasuk latihan Stata dengan auto.dta."
    }
  ],

  /* -----------------------------------------------------------------------
     4. Appearance of the embedded comments. Safe to leave alone.
     ----------------------------------------------------------------------- */
  commentsLimit: 20,
  colorful: true
};
