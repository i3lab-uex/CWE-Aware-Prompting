import html

# Pre‑defined HTML template for a forum post.
# The placeholders {title}, {body} and {points} will be replaced with
# the escaped user content.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {points}
</div>
"""

def create_forum_entry(title: str, body: str, points: list[str]) -> str:
    """
    Assemble a sanitized forum post.

    Parameters
    ----------
    title : str
        The title or main topic of the forum post.
    body : str
        The primary content or body text of the post.
    points : list[str]
        A series of user‑supplied discussion points or options in
        markdown format.  They will be rendered as an unordered list.

    Returns
    -------
    str
        A fully formatted and sanitized forum post ready for display.
    """
    # Escape all user input to prevent XSS (CWE‑79).
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Convert points to a list of escaped <li> items.
    if points:
        safe_items = [
            f"<li>{html.escape(p, quote=True)}</li>" for p in points
        ]
        points_html = f"<ul>\n{''.join(safe_items)}\n</ul>"
    else:
        points_html = ""

    # Format the final HTML string.
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )