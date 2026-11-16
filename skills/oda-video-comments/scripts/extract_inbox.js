// Read-only extractor for the YouTube Studio comments inbox.
// Run with the Claude in Chrome javascript tool on
//   https://studio.youtube.com/channel/<channel_id>/comments/inbox
// It only reads the page's own data; it clicks, types and changes nothing.
//
// The result is JSON: {channel, count, threads:[{comment_id, video_id, video_title,
//   author, author_is_owner, published, text, likes, reply_count, replies:[...]}]}
//
// Paging: the javascript tool truncates results at about 1,000 characters, so this script
// keeps the full JSON in the page and returns it in chunks. It returns
//   PAGE 1/<n> <first chunk>
// Fetch the rest with one javascript call per chunk:
//   window.__odaVideoComments.page(2)   ...   window.__odaVideoComments.page(<n>)
// and join the chunks in order, with nothing in between, before parsing the JSON.
//
// The Chrome extension also blocks any result containing a URL with a query string, so:
//  - it returns IDs, not URLs. Build the comment link as
//    https://www.youtube.com/watch?v=<video_id>&lc=<comment_id>;
//  - query strings in comment text are rewritten as "<url> [query k: v | k: v]", for example
//    "https://www.youtube.com/watch [query v: xLdFY9mGJxI | t: 168s]"; fragments are dropped.
//    reply_diff.py turns these back into real URLs. To rebuild one by hand, swap
//    " [query " for "?", " | " for "&" and ": " for "=", and drop the "]".
//    (Tested 2026-11-16: the extension blocks "k=v ; k=v" but allows "k: v | k: v".)
(() => {
  const PAGE = 900;
  const defang = (s) => s
    .replace(/(https?:\/\/[^\s?#]+)\?([^\s#]*)(#\S*)?/g, (m, base, q) =>
      `${base} [query ${q.split("&").filter(Boolean).map(p => p.replace("=", ": ")).join(" | ")}]`)
    .replace(/(https?:\/\/[^\s#]+)#\S*/g, "$1");
  const runs = (t) => defang(!t ? "" : (t.simpleText != null ? t.simpleText : (t.runs || []).map(r => r.text).join("")));
  const dataOf = (el) => el && (el.data || el.comment || (el.__data && (el.__data.comment || el.__data.data))) || null;
  const one = (el) => {
    const c = dataOf(el);
    if (!c) return null;
    const j = JSON.stringify(c);
    return {
      comment_id: c.commentId,
      video_id: (j.match(/"videoId":"([^"]+)"/) || [])[1] || null,
      author: runs(c.authorText),
      author_is_owner: !!c.authorIsChannelOwner,
      published: runs(c.publishedTimeText),
      text: runs(c.contentText),
      likes: runs(c.voteCount) || "0",
    };
  };
  const threads = [...document.querySelectorAll("ytcp-comment-thread")].map((th) => {
    const all = [...th.querySelectorAll("ytcp-comment")];
    const top = one(all[0]);
    if (!top) return null;
    const title = [...th.querySelectorAll("a")].map(a => a.textContent.trim())
      .filter(t => t && !t.startsWith("@")).pop() || null;
    const replyBtn = [...th.querySelectorAll("*")].map(e => e.childElementCount === 0 ? e.textContent.trim() : "")
      .find(t => /^\d+ repl(y|ies)$/.test(t));
    return Object.assign(top, {
      video_title: title,
      reply_count: replyBtn ? parseInt(replyBtn, 10) : null,
      replies: all.slice(1).map(one).filter(Boolean),
    });
  }).filter(Boolean);
  const channel = (document.querySelector("#entity-name, .entity-name") || {}).textContent;
  const json = JSON.stringify({ channel: channel ? channel.trim() : null, count: threads.length, threads });
  const pages = Math.max(1, Math.ceil(json.length / PAGE));
  window.__odaVideoComments = {
    json,
    pages,
    page: (n) => `PAGE ${n}/${pages} ` + json.slice((n - 1) * PAGE, n * PAGE),
  };
  return window.__odaVideoComments.page(1);
})()
