import html

# Pre‑defined HTML template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-content">{body}</div>
  <ul class="discussion-points">
    {points}
  </ul>
</div>
"""

def build_forum_post(headline: str, content: str, items: list[str]) -> str:
    """
    Assemble a sanitized forum post.

    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary content or body text of the post.
    items : list[str]
        A series of user‑supplied discussion points or options in markdown
        format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string representing the forum post.
    """
    # Escape user input to prevent XSS
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Convert each markdown item to an HTML list element
    safe_points = []
    for item in items:
        escaped_item = html.escape(item, quote=True)
        safe_points.append(f"<li>{escaped_item}</li>")
    points_html = "\n".join(safe_points)

    # Populate the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )