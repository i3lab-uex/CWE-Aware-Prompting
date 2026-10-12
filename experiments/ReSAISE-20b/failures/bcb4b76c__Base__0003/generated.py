import html

# Predefined HTML template for forum posts.
# It contains three placeholders: {title}, {body} and {points}
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  <ul class="discussion-points">{points}</ul>
</div>
"""

def create_forum_post(topic: str, text_body: str, points: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic : str
        The title or main topic of the forum post.
    text_body : str
        The main body/content of the forum post.
    points : list[str]
        A collection of user-provided discussion points or options in markdown
        format. The function will escape any HTML special characters to prevent
        XSS attacks.

    Returns
    -------
    str
        The fully formatted and sanitized HTML representation of the forum post.
    """
    # Escape user-provided content to neutralize XSS vectors
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=True)

    # Convert each point into a <li> element with escaped content
    safe_points_items = [
        f"<li>{html.escape(point, quote=True)}</li>" for point in points
    ]
    safe_points = "\n".join(safe_points_items)

    # Build the final HTML using the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )