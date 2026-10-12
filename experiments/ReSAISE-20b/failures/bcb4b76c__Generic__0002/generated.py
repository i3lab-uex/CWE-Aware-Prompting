import html
from typing import List

# Example template – replace with the actual one in your project.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  <ul>{points}</ul>
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
        A collection of user‑provided discussion points or options in markdown format.

    Returns
    -------
    str
        A string containing the fully formatted and sanitized HTML representation of the forum post.
    """
    # Escape all user‑supplied content to prevent XSS
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=True)

    # Convert markdown points to plain text and escape
    safe_points_html = ""
    for point in points:
        escaped_point = html.escape(point, quote=True)
        safe_points_html += f"<li>{escaped_point}</li>"

    # Build final HTML using the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points_html
    )