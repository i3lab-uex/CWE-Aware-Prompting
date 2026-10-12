import html
from typing import List

# Predefined HTML template for forum posts.
# The placeholders {title}, {body}, and {points} will be replaced
# with the escaped title, body, and formatted discussion points respectively.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {points}
</div>
"""

def build_forum_entry(post_title: str, post_body: str,
                      bullet_points: List[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : list[str]
        A collection of user‑provided discussion points or options in markdown format.

    Returns
    -------
    str
        A string containing the fully formatted and sanitized HTML representation of the forum post.
    """
    # Sanitize title and body by escaping all HTML special characters
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Convert each bullet point to a list item, escaping its content.
    safe_points = ""
    if bullet_points:
        escaped_items = [f"<li>{html.escape(point, quote=True)}</li>"
                         for point in bullet_points]
        safe_points = "<ul>\n" + "\n".join(escaped_items) + "\n</ul>"

    # Format the final HTML using the predefined template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )