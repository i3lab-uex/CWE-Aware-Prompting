import html
from typing import List

# Example template for a forum post.  The placeholders are marked with curly braces.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul class="discussion-points">
        {points}
    </ul>
</div>
"""

def create_forum_entry(title: str, body: str, points: List[str]) -> str:
    """
    Assemble a forum post from user supplied content.

    Parameters
    ----------
    title : str
        The main topic of the post.
    body : str
        The primary content of the post.
    points : list[str]
        A series of discussion points.  Each point is expected to be in Markdown
        format, but it will be escaped for safe HTML rendering.

    Returns
    -------
    str
        The fully formatted, sanitized forum post ready for display.
    """
    # Escape all user supplied content to neutralise special characters
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Convert each point into a list item.  Each point is escaped to prevent
    # injection of arbitrary HTML or JavaScript.
    safe_points = []
    for point in points:
        escaped_point = html.escape(point, quote=True)
        safe_points.append(f"<li>{escaped_point}</li>")
    points_html = "\n".join(safe_points)

    # Render the final HTML using the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )