import html

# Predefined template for forum posts.
# Placeholders: {title} for the headline, {body} for the main content,
# and {list} for the discussion points rendered as an unordered list.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
    <ul>{list}</ul>
</div>
"""

def build_forum_post(headline: str, content: str, items: list[str]) -> str:
    """
    Assemble a sanitized forum post from the given headline, content,
    and discussion items.

    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary body text of the post.
    items : list[str]
        A series of discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized forum post as an HTML string.

    Notes
    -----
    - All user-provided strings are escaped to mitigate XSS (CWE-79).
    - Markdown is not rendered; it is treated as plain text.
    """
    # Escape headline and content to neutralize any HTML or script tags
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the list items. Each item is escaped and wrapped in <li> tags.
    safe_items = []
    for item in items:
        escaped_item = html.escape(item, quote=True)
        safe_items.append(f"<li>{escaped_item}</li>")

    # Join the list items into a single string
    safe_list = "\n".join(safe_items)

    # Format the final HTML using the predefined template
    forum_post = FORUM_POST_FORMAT.format(
        title=safe_headline,
        body=safe_content,
        list=safe_list
    )

    return forum_post.strip()