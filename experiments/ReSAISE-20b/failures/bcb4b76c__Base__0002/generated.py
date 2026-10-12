import html

# Predefined HTML template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  {points_section}
</div>
"""

def _render_points(points: list[str]) -> str:
    """
    Render a list of discussion points as an unordered HTML list.
    Each point is escaped to prevent XSS attacks.
    """
    if not points:
        return ""

    list_items = []
    for point in points:
        # Escape any HTML special characters.
        escaped_point = html.escape(point, quote=True)
        list_items.append(f"<li>{escaped_point}</li>")

    points_html = "<ul>\n" + "\n".join(list_items) + "\n</ul>"
    return f"<div class=\"discussion-points\">\n{points_html}\n</div>"

def create_forum_post(topic: str, text_body: str, points: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic : str
        The title or main topic of the forum post.
    text_body : str
        The main body/content of the forum post.
    points : list[str]
        A collection of user-provided discussion points or options in markdown format.

    Returns
    -------
    str
        A string containing the fully formatted and sanitized HTML representation of the forum post.
    """
    # Escape user input to prevent XSS (CWE-79).
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=True)

    # Render the points section (may be empty).
    points_section = _render_points(points)

    # Substitute placeholders in the template.
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points_section=points_section
    )