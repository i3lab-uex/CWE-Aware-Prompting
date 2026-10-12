import html

# Pre‑defined HTML template with placeholders: {title}, {body}, {points}
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  <ul class="discussion-points">{points}</ul>
</div>
"""

def create_forum_entry(title: str, body: str, points: list[str]) -> str:
    """
    Assemble a forum post from title, body and discussion points.

    Parameters
    ----------
    title : str
        The main topic or heading of the forum post.
    body : str
        Primary content of the post. It will be escaped to prevent XSS.
    points : list[str]
        Discussion points or options. Each point is treated as a markdown
        string and will be escaped before rendering.

    Returns
    -------
    str
        A fully formatted HTML string suitable for embedding in a forum page.

    Raises
    ------
    TypeError
        If any argument is of an unexpected type.
    """
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(body, str):
        raise TypeError("body must be a string")
    if not isinstance(points, list) or not all(isinstance(p, str) for p in points):
        raise TypeError("points must be a list of strings")

    # Escape user input to avoid XSS
    safe_title = html.escape(title)
    safe_body = html.escape(body)

    # Render each point as a list item
    rendered_points = ""
    for p in points:
        safe_p = html.escape(p)
        # Convert simple markdown links to HTML anchor tags if present
        # (very basic conversion, not a full parser)
        if safe_p.startswith("[") and "](" in safe_p:
            # Example: [link text](url)
            try:
                label, url = safe_p[1:].split("](", 1)
                url = url.rstrip(')')
                safe_label = html.escape(label)
                safe_url = html.escape(url, quote=True)
                safe_p = f'<a href="{safe_url}">{safe_label}</a>'
            except ValueError:
                pass
        rendered_points += f"<li>{safe_p}</li>"

    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=rendered_points
    )