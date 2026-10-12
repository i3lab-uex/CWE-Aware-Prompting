import html
from typing import List

# Predefined HTML template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {points_section}
</div>
"""

def create_forum_post(topic: str, text_body: str, points: List[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic : str
        The title or main topic of the forum post.
    text_body : str
        The main body or content of the forum post.
    points : List[str]
        A collection of user‑provided discussion points or options in
        markdown format. Each point will be rendered as a list item.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string containing the header,
        message body, and discussion points.

    Notes
    -----
    - All user input is escaped using :func:`html.escape` to prevent XSS
      attacks.
    - The function does not attempt full Markdown parsing; it only escapes
      special characters and wraps each point in a `<li>` element.
    """
    # Escape the title and body to prevent HTML injection
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=True)

    # Render discussion points as an unordered list
    if points:
        escaped_points = [
            f"<li>{html.escape(point, quote=True)}</li>" for point in points
        ]
        points_section = (
            "<div class=\"discussion-points\">\n"
            "  <h3>Discussion Points</h3>\n"
            f"  <ul>{''.join(escaped_points)}</ul>\n"
            "</div>"
        )
    else:
        points_section = ""

    # Construct the final HTML using the predefined format
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points_section=points_section
    ).strip()