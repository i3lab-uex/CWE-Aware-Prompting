import html
from typing import List

# Example template – adjust placeholders to match your actual format.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  <ul>{points}</ul>
</div>
"""

def build_forum_entry(
    post_title: str,
    post_body: str,
    bullet_points: List[str],
) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : list[str]
        A collection of user-provided discussion points or options in markdown format.

    Returns
    -------
    str
        A string containing the fully formatted and sanitized HTML representation of the forum post.
    """
    # Sanitize title and body to prevent XSS attacks
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Convert markdown bullet points to HTML list items
    safe_points = []
    for point in bullet_points:
        # Escape the markdown content first
        escaped_point = html.escape(point, quote=True)
        safe_points.append(f"<li>{escaped_point}</li>")

    # Join list items into a single string
    points_html = "".join(safe_points)

    # Format the final HTML using the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )