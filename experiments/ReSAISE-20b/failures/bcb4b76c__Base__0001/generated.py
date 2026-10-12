import html
from typing import List

# Example template: adjust placeholders as needed for your application.
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

    Args:
        topic: The title or main topic of the forum post.
        text_body: The main body/content of the forum post.
        points: A list of discussion points (markdown format) to be rendered as <li> elements.

    Returns:
        A string containing the fully formatted and sanitized HTML representation of the forum post.
    """
    # Escape user-supplied data to prevent XSS
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=True)

    # Render each point as a sanitized <li> element
    safe_points = []
    for pt in points:
        escaped_pt = html.escape(pt, quote=True)
        safe_points.append(f"<li>{escaped_pt}</li>")

    points_html = "\n".join(safe_points)

    # Combine into the final HTML using the template
    return FORUM_POST_FORMAT.format(title=safe_title, body=safe_body, points=points_html)