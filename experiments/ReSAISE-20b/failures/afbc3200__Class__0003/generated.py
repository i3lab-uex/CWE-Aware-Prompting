import html

# Predefined HTML template for forum posts.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  <ul class="discussion-points">
    {points}
  </ul>
</div>
"""

def build_forum_entry(post_title: str, post_body: str, bullet_points: list[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : list[str]
        A collection of user-provided discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML representation of the forum post.

    Notes
    -----
    - All user input is escaped using html.escape to mitigate CWE-74.
    - Markdown in bullet points is not rendered; it is treated as plain text for safety.
    """
    # Escape all user-provided content
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Convert each bullet point to a <li> element with escaped content
    safe_points = []
    for point in bullet_points:
        escaped_point = html.escape(point, quote=True)
        safe_points.append(f"<li>{escaped_point}</li>")
    points_html = "\n".join(safe_points)

    # Format the final HTML
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )