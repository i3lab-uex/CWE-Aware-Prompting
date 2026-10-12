import html

# Pre‑defined template for a forum post.  The placeholders are filled with
# escaped content to avoid XSS.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points_section}
</div>
"""

def create_forum_entry(title: str, body: str, points: list[str]) -> str:
    """
    Assemble a sanitized forum post.

    Parameters
    ----------
    title : str
        The main topic or title of the forum post.
    body : str
        The primary content of the post.  It may contain user‑generated text.
    points : list[str]
        A list of discussion points or options, provided in markdown format.

    Returns
    -------
    str
        A complete HTML string that safely renders the post and its points.
    """
    # Escape all user‑provided content to neutralise potential XSS vectors
    escaped_title = html.escape(title, quote=True)
    escaped_body = html.escape(body, quote=True)

    # Build the unordered list of points
    if points:
        escaped_points = []
        for p in points:
            # Escape each point individually
            escaped_p = html.escape(p, quote=True)
            escaped_points.append(f"<li>{escaped_p}</li>")
        points_section = (
            f'<ul class="discussion-points">\n' + "\n".join(escaped_points) + "\n</ul>"
        )
    else:
        points_section = ""

    # Format the final HTML using the template
    forum_post_html = FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        points_section=points_section
    )
    return forum_post_html.strip()