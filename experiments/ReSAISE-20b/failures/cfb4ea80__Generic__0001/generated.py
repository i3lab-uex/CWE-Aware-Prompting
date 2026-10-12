import html

# Pre‑defined HTML template for a forum post.
# The placeholders `{title}`, `{body}` and `{points}` will be replaced
# by the formatted title, body text and discussion points respectively.
FORUM_POST_FORMAT = """
<article class="forum-post">
  <header>
    <h2>{title}</h2>
  </header>
  <section class="post-body">
    {body}
  </section>
  <footer class="discussion-points">
    <h3>Discussion Points</h3>
    {points}
  </footer>
</article>
"""

def create_forum_entry(title: str, body: str, points: list[str]) -> str:
    """
    Assemble a structured forum post using user-provided content.

    Parameters
    ----------
    title : str
        The title or main topic of the forum post.
    body : str
        The primary content or body text of the post.
    points : list[str]
        A series of user-supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized forum post as an HTML string.

    Notes
    -----
    * All user-supplied content is escaped to prevent XSS.
    * Markdown syntax in `points` is preserved; only HTML special
      characters are escaped.
    """
    # Sanitize title and body to prevent XSS
    safe_title = html.escape(title)
    safe_body = html.escape(body).replace("\n", "<br>")

    # Convert points to an unordered list
    if not points:
        safe_points = "<p>No discussion points provided.</p>"
    else:
        list_items = []
        for p in points:
            # Escape each point and preserve line breaks
            escaped_point = html.escape(p).replace("\n", "<br>")
            list_items.append(f"<li>{escaped_point}</li>")
        safe_points = f"<ul>\n{''.join(list_items)}\n</ul>"

    # Render the final post using the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )