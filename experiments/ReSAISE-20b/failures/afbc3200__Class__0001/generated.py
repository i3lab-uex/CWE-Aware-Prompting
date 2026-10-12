import html
from typing import List

# Example template; in real usage this would be defined elsewhere.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points}
</div>
"""

def build_forum_entry(
    post_title: str,
    post_body: str,
    bullet_points: List[str]
) -> str:
    """
    Construct a sanitized HTML representation of a forum post.

    Args:
        post_title: The title or main topic of the forum post.
        post_body: The main body or content of the forum post.
        bullet_points: A list of discussion points or options.

    Returns:
        A string containing the fully formatted and sanitized HTML
        representation of the forum post.
    """
    # Sanitize title and body to prevent injection (CWE-74)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Build the unordered list of bullet points
    if bullet_points:
        safe_items = []
        for point in bullet_points:
            # Escape each point; preserve markdown if desired by converting
            # to plain text (no HTML tags).
            safe_point = html.escape(point, quote=True)
            safe_items.append(f"<li>{safe_point}</li>")
        points_html = f"\n<ul>\n{''.join(safe_items)}\n</ul>"
    else:
        points_html = ""

    # Render the final template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )