import html

# Pre‑defined HTML template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  <ul class="discussion-points">
    {points}
  </ul>
</div>
"""

def create_forum_entry(title: str, body: str, points: list[str]) -> str:
    """
    Assemble a structured forum post.

    Parameters
    ----------
    title : str
        The title or main topic of the forum post.
    body : str
        The primary content or body text of the post.
    points : list[str]
        A series of user‑supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized forum post string ready for HTML rendering.

    Raises
    ------
    ValueError
        If any argument is not of the expected type.
    """
    # Basic type validation
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(body, str):
        raise ValueError("body must be a string")
    if not isinstance(points, list) or not all(isinstance(p, str) for p in points):
        raise ValueError("points must be a list of strings")

    # Escape user input to prevent XSS
    escaped_title = html.escape(title, quote=True)
    escaped_body = html.escape(body, quote=True)

    # Convert markdown points to plain text and escape them
    escaped_points = []
    for point in points:
        # Simple markdown removal: strip leading list markers and escape
        cleaned = point.lstrip("-*+ ").strip()
        escaped_points.append(f"<li>{html.escape(cleaned, quote=True)}</li>")

    points_html = "\n".join(escaped_points)

    # Format the final post
    return FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        points=points_html
    )