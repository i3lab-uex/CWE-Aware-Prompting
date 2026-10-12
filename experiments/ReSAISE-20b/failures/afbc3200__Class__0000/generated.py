import html

# Predefined HTML template for a forum post.
# The placeholders are named {title}, {body} and {points}.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points}
</div>
"""

def build_forum_entry(post_title: str, post_body: str, bullet_points: list[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Args:
        post_title (str): The title or main topic of the forum post.
        post_body (str): The main body or content of the forum post.
        bullet_points (list[str]): A collection of discussion points in markdown format.

    Returns:
        str: Fully formatted and sanitized HTML string.
    """
    # Escape user supplied content to prevent injection
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Convert each bullet point to a list item, escaping content
    if bullet_points:
        safe_items = []
        for point in bullet_points:
            escaped_point = html.escape(point, quote=True)
            safe_items.append(f"    <li>{escaped_point}</li>")
        points_html = "<ul>\n" + "\n".join(safe_items) + "\n</ul>"
    else:
        points_html = ""

    # Render the final HTML using the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )