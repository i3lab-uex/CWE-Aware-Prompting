import html
from typing import List

# A minimal HTML template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  <ul>{points_list}</ul>
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
    points : list[str]
        A collection of user‑provided discussion points or options
        in markdown format.  The function will escape any HTML special
        characters to prevent injection attacks.

    Returns
    -------
    str
        The fully formatted and sanitized HTML representation of the forum post.
    """
    # Sanitize title and body to avoid XSS
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=True)

    # Convert each point to a safe list item.
    # We only escape the content; any markdown is left as plain text
    # to avoid executing unintended markup.
    safe_points = []
    for point in points:
        escaped_point = html.escape(point, quote=True)
        safe_points.append(f"<li>{escaped_point}</li>")

    points_html = "\n".join(safe_points)

    # Render the final HTML using the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points_list=points_html
    )