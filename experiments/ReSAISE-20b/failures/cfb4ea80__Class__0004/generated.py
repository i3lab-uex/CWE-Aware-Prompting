import html

# Pre‑defined HTML template for forum posts.
# The placeholders are `{title}`, `{body}` and `{points}`.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
    <ul class="discussion-points">
        {points}
    </ul>
</div>
"""

def create_forum_entry(title: str, body: str, points: list[str]) -> str:
    """
    Assemble a sanitized forum post from user‑provided content.

    Parameters
    ----------
    title : str
        The main topic or title of the forum post.
    body : str
        The primary content of the post.
    points : list[str]
        A list of discussion points or options, each as a Markdown string.

    Returns
    -------
    str
        The fully formatted and escaped HTML forum post.
    """
    # Escape title and body to prevent injection attacks (CWE‑74).
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Render each point as an <li>, escaping its content.
    list_items = []
    for p in points:
        escaped_p = html.escape(p, quote=True)
        list_items.append(f"<li>{escaped_p}</li>")
    safe_points = "\n".join(list_items)

    # Populate the template with sanitized values.
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )