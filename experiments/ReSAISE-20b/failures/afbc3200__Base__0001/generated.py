import html

# Example template; replace with the actual format used in your application.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points_section}
</div>
"""

def build_forum_entry(post_title: str,
                      post_body: str,
                      bullet_points: list[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : list[str]
        A collection of user-provided discussion points or options in markdown
        format.

    Returns
    -------
    str
        A string containing the fully formatted and sanitized HTML representation
        of the forum post, including header, message body, and safely rendered
        discussion points.

    Notes
    -----
    All user input is escaped using :func:`html.escape` to prevent XSS
    (CWE-79). The function does not perform Markdown conversion; it only
    ensures the bullet points are safely rendered as plain text within <li>
    elements. If Markdown rendering is required, consider using a safe
    library such as `markdown2` with the `safe_mode='escape'` option.
    """
    # Escape title and body to neutralize HTML special characters
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Convert bullet points to <ul> list; escape each point
    if bullet_points:
        escaped_items = [
            f"<li>{html.escape(point, quote=True)}</li>"
            for point in bullet_points
        ]
        points_section = f"<ul>{''.join(escaped_items)}</ul>"
    else:
        points_section = ""

    # Populate the template
    rendered_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points_section=points_section
    )

    return rendered_html.strip()