import html

# Predefined HTML template for forum posts.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points_section}
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
        The main body or content of the forum post.
    points : list[str]
        A collection of user-provided discussion points or options in markdown format.

    Returns
    -------
    str
        A string containing the fully formatted and sanitized HTML representation of the forum post,
        including the header, message body, and safely rendered discussion points.

    Notes
    -----
    * All user input is escaped using `html.escape` to avoid XSS or HTML injection.
    * The function does **not** perform full markdown parsing; it simply escapes the content
      and places each point inside an `<li>` element.
    * The resulting HTML is safe for inclusion in a page that does not perform additional
      transformations on the content.
    """
    # Sanitize title and body
    safe_title = html.escape(topic, quote=True)
    safe_body = html.escape(text_body, quote=False)

    # Build the points section
    if points:
        escaped_points = "".join(
            f"<li>{html.escape(point, quote=False)}</li>" for point in points
        )
        points_section = f"<ul>{escaped_points}</ul>"
    else:
        points_section = ""

    # Format the final HTML
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points_section=points_section
    )