import html

# Pre‑defined HTML template for a forum post.
# The placeholders {title}, {body} and {points} will be replaced by the function.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
    {points}
</div>
"""

def compile_post(subject: str, text: str, highlights: list[str]) -> str:
    """
    Assemble a sanitized forum post from user supplied components.

    Parameters
    ----------
    subject : str
        The title or main topic of the forum post.
    text : str
        The primary content or body text of the post.
    highlights : list[str]
        A series of discussion points or options. Each item may contain
        Markdown; only a minimal safe rendering is performed.

    Returns
    -------
    str
        The fully formatted and sanitized forum post as an HTML string.
    """
    # Sanitize title and body to avoid XSS.
    safe_title = html.escape(subject, quote=True)
    safe_body  = html.escape(text, quote=True)

    # Convert each highlight into a safe <li> element.
    list_items = []
    for item in highlights:
        # Escape the content; no Markdown parsing is performed to keep it safe.
        escaped_item = html.escape(item, quote=True)
        list_items.append(f"<li>{escaped_item}</li>")

    # Build the unordered list if any highlights were provided.
    points_html = ""
    if list_items:
        points_html = f"<ul>{''.join(list_items)}</ul>"

    # Format the final HTML using the predefined template.
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )

    return post_html.strip()