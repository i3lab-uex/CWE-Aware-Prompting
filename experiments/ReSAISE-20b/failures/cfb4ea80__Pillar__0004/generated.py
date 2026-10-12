import html
from typing import List

# Pre‑defined HTML template for forum posts.
FORUM_POST_FORMAT = """
<article class="forum-post">
  <header>
    <h1>{title}</h1>
  </header>
  <section class="content">
    {body}
  </section>
  <aside class="discussion-points">
    <h2>Discussion Points</h2>
    {points}
  </aside>
</article>
"""

def create_forum_entry(title: str, body: str, points: List[str]) -> str:
    """
    Assemble a sanitized forum post from the given title, body and discussion points.

    Parameters
    ----------
    title : str
        The title or main topic of the forum post.
    body : str
        The primary content or body text of the post. Markdown is treated as plain text.
    points : list[str]
        A series of user‑supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized forum post, with the title, body and discussion points.

    Notes
    -----
    * All user supplied text is escaped using ``html.escape`` to prevent HTML injection.
    * The function does not attempt to parse Markdown; it treats the content as plain text
      and renders it inside a ``<p>`` element.  This mitigates CWE‑707 by ensuring that
      the output is well‑formed HTML and not influenced by malicious markup.
    """
    # Escape user input to avoid XSS / malformed HTML
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Render discussion points as a list
    if not points:
        safe_points = "<p>No discussion points provided.</p>"
    else:
        list_items = []
        for point in points:
            escaped_point = html.escape(point, quote=True)
            list_items.append(f"<li>{escaped_point}</li>")
        safe_points = "<ul>\n" + "\n".join(list_items) + "\n</ul>"

    # Format the final post
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=f"<p>{safe_body}</p>",
        points=safe_points
    )