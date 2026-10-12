import html

# Pre‑defined HTML template for a forum post.
# The placeholders are `{title}`, `{content}` and `{items}`.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{content}</div>
    <ul class="discussion-points">
        {items}
    </ul>
</div>
"""

def build_forum_post(headline: str, content: str, items: list[str]) -> str:
    """
    Assemble a forum post from user supplied parts.

    Parameters
    ----------
    headline : str
        Title of the forum post.
    content : str
        Body text of the post.
    items : list[str]
        Discussion points or options, each in markdown format.

    Returns
    -------
    str
        Fully formatted HTML post with user input safely escaped.
    """
    # Escape title and body to avoid XSS
    safe_title = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Convert each discussion item to a list element.
    # We escape the entire string; if markdown is desired it should be rendered
    # on the client side after proper sanitization.
    list_items = []
    for item in items:
        escaped_item = html.escape(item, quote=True)
        list_items.append(f"<li>{escaped_item}</li>")
    safe_items = "\n".join(list_items)

    # Build final HTML
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        content=safe_content,
        items=safe_items
    )