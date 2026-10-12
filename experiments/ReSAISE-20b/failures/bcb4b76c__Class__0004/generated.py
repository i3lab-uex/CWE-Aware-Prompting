import html

# Predefined HTML template for forum posts.
# Placeholders: {title}, {body}, {points}
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul class="discussion-points">
        {points}
    </ul>
</div>
"""

def create_forum_post(topic: str, text_body: str, points: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Args:
        topic: The title or main topic of the forum post.
        text_body: The main body/content of the forum post.
        points: A list of user-provided discussion points (markdown format).

    Returns:
        A string containing the fully formatted and sanitized HTML representation
        of the forum post, including header, message body, and safely rendered
        discussion points.

    Raises:
        ValueError: If any argument is of an unexpected type.
    """
    if not isinstance(topic, str):
        raise ValueError("topic must be a string")
    if not isinstance(text_body, str):
        raise ValueError("text_body must be a string")
    if not isinstance(points, list) or not all(isinstance(p, str) for p in points):
        raise ValueError("points must be a list of strings")

    # Escape special HTML characters to prevent injection.
    escaped_title = html.escape(topic, quote=True)
    escaped_body = html.escape(text_body, quote=True)

    # Convert each point to an <li> element after escaping.
    escaped_points = []
    for p in points:
        # Escape any HTML special characters in the point.
        escaped_p = html.escape(p, quote=True)
        # Convert markdown line breaks or list markers if needed.
        escaped_points.append(f"<li>{escaped_p}</li>")

    points_html = "\n".join(escaped_points)

    # Format the final HTML using the template.
    formatted_post = FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        points=points_html
    )

    return formatted_post.strip()