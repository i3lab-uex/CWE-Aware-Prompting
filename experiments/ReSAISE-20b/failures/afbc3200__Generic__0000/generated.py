import html

# Predefined HTML template for a forum post.
# The placeholders {title}, {body} and {points} will be replaced
# by the sanitized content of the forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points}
</div>
"""

def build_forum_entry(post_title: str, post_body: str, bullet_points: list[str]) -> str:
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
        A fully formatted and sanitized HTML representation of the forum post,
        including the header, message body, and safely rendered discussion points.

    Notes
    -----
    * All user input is escaped using `html.escape` to prevent XSS attacks.
    * Markdown in bullet points is not parsed; it is treated as plain text.
    """
    # Sanitize the title and body
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Build the unordered list of discussion points
    if bullet_points:
        # Each point is escaped individually
        safe_items = [
            f"<li>{html.escape(point, quote=True)}</li>" for point in bullet_points
        ]
        points_html = f"<ul>{''.join(safe_items)}</ul>"
    else:
        points_html = ""

    # Insert the sanitized parts into the template
    return FORUM_POST_FORMAT.format(title=safe_title, body=safe_body, points=points_html)