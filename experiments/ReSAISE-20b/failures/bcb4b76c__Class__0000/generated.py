import html

# Predefined HTML template for a forum post.
# {title}  → the title of the post
# {body}   → the main body content
# {points} → an unordered list of discussion points
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points}
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
        The main body content of the forum post.
    points : list[str]
        A collection of user-provided discussion points or options
        in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string containing the post title,
        body, and discussion points rendered as an unordered list.

    Raises
    ------
    TypeError
        If any of the arguments are not of the expected type.
    """
    # Validate argument types
    if not isinstance(topic, str):
        raise TypeError("topic must be a string")
    if not isinstance(text_body, str):
        raise TypeError("text_body must be a string")
    if not isinstance(points, list) or not all(isinstance(p, str) for p in points):
        raise TypeError("points must be a list of strings")

    # Escape user input to prevent injection (CWE-74)
    escaped_title = html.escape(topic, quote=True)
    escaped_body = html.escape(text_body, quote=True)

    # Build the unordered list of discussion points
    if points:
        escaped_points = [
            f"<li>{html.escape(p, quote=True)}</li>" for p in points
        ]
        ul_html = f"<ul>{''.join(escaped_points)}</ul>"
    else:
        # If no points are provided, omit the list entirely
        ul_html = ""

    # Format the final HTML using the predefined template
    formatted_post = FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        points=ul_html
    )

    return formatted_post.strip()