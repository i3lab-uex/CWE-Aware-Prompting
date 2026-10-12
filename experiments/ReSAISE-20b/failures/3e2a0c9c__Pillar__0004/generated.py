import html

# Predefined HTML template for forum posts.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {list_section}
</div>
"""

def build_post_html(topic_title: str, body_text: str, list_items: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main content/body of the forum post.
    list_items : list[str]
        A collection of discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized HTML representation of the forum post.
    """
    # Escape title and body to avoid injection
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Build the unordered list if items are provided
    if list_items:
        safe_list = "<ul>"
        for item in list_items:
            # Escape each markdown string; do not render markdown to avoid XSS
            safe_item = html.escape(item, quote=True)
            safe_list += f"<li>{safe_item}</li>"
        safe_list += "</ul>"
    else:
        safe_list = ""

    # Format the final HTML
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        list_section=safe_list
    )
    return post_html.strip()