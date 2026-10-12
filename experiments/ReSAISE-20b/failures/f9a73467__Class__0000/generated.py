import html

# Predefined HTML template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul class="discussion-points">
        {points}
    </ul>
</div>
"""

def compile_post(subject: str, text: str, highlights: list[str]) -> str:
    """
    Assemble a forum post from user-provided content.

    Parameters
    ----------
    subject : str
        The title or main topic of the forum post.
    text : str
        The primary content or body text of the post.
    highlights : list[str]
        A series of user-supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string representing the forum post.
    """
    # Sanitize title, body, and each highlight to prevent HTML injection
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(text, quote=True)

    # Convert each highlight to an <li> element after escaping.
    safe_points = []
    for point in highlights:
        escaped_point = html.escape(point, quote=True)
        safe_points.append(f"<li>{escaped_point}</li>")

    # Join the list items into a single string.
    points_html = "\n        ".join(safe_points)

    # Render the final HTML using the template.
    rendered = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )

    return rendered.strip()