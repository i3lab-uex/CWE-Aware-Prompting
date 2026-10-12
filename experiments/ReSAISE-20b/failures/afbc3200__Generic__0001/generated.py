import html
from typing import List

# A simple HTML template for a forum post.
# Placeholders: {title}, {body}, {points}
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points}
</div>
"""

def build_forum_entry(post_title: str,
                      post_body: str,
                      bullet_points: List[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Args:
        post_title: Title or main topic of the forum post.
        post_body: Main body or content of the forum post.
        bullet_points: A list of discussion points in markdown format.

    Returns:
        str: Fully formatted and sanitized HTML string.
    """
    # Escape title and body to avoid XSS
    safe_title = html.escape(post_title)
    safe_body = html.escape(post_body)

    # Convert markdown bullet points to <li> elements.
    list_items = []
    for point in bullet_points:
        # Escape the content first
        escaped_point = html.escape(point)
        list_items.append(f"<li>{escaped_point}</li>")

    if list_items:
        points_html = f"<ul>\n{''.join(list_items)}\n</ul>"
    else:
        points_html = ""

    # Format the final HTML
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )