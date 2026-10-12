import html

# A simple HTML template for forum posts.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {points}
</div>
"""

def build_forum_entry(post_title: str, post_body: str, bullet_points: list[str]) -> str:
    """
    Construct a sanitized HTML representation of a forum post.

    Args:
        post_title: The title or main topic of the forum post.
        post_body: The main body or content of the forum post.
        bullet_points: A list of discussion points in markdown format.

    Returns:
        A string containing the fully formatted and sanitized HTML representation
        of the forum post.
    """
    # Escape user-provided content to prevent XSS (CWE‑79).
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Render discussion points as an unordered list.
    if bullet_points:
        escaped_items = [
            f"<li>{html.escape(point, quote=True)}</li>"
            for point in bullet_points
        ]
        points_html = f"<ul>{''.join(escaped_items)}</ul>"
    else:
        points_html = ""

    # Substitute into the template.
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )