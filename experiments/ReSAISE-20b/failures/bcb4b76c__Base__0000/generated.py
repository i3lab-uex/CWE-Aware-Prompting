import html

# Predefined HTML template with placeholders for title, body and points.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {points_section}
</div>
"""

def create_forum_post(topic: str, text_body: str, points: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic : str
        The title or main topic of the forum post.
    text_body : str
        The main body or content of the forum post.
    points : list[str]
        A collection of user‑provided discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML representation of the forum post.
    """
    # Escape user inputs to prevent XSS
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=True)

    # Build the unordered list of points
    if points:
        escaped_points = [f"<li>{html.escape(p, quote=True)}</li>" for p in points]
        points_section = f"<ul>{''.join(escaped_points)}</ul>"
    else:
        points_section = ""

    # Populate the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points_section=points_section
    )