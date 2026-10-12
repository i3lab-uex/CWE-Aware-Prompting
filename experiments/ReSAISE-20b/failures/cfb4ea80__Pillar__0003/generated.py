import html

# Pre‑defined HTML template for forum posts.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  {points}
</div>
"""

def create_forum_entry(title: str, body: str, points: list[str]) -> str:
    """
    Assemble a forum post from the supplied title, body and discussion points.

    Parameters
    ----------
    title : str
        The main topic or header of the post.
    body : str
        The primary content/body of the post.
    points : list[str]
        Discussion points or options. Each element is expected to be in
        markdown format but will be escaped for safe HTML rendering.

    Returns
    -------
    str
        A fully formatted, sanitized forum post string.
    """
    # Sanitize the title and body to prevent HTML injection
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Convert each point to a list item after escaping
    if points:
        escaped_points = [f"<li>{html.escape(p, quote=True)}</li>" for p in points]
        list_items = "\n".join(escaped_points)
        safe_points_html = f"<ul>\n{list_items}\n</ul>"
    else:
        safe_points_html = ""

    # Render the final post
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points_html
    )