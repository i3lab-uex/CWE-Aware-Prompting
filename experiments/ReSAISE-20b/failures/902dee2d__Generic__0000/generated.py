import html
from typing import List

# Pre‑defined template for a forum post.
# It contains three placeholders: {title}, {body} and {points}
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul class="discussion-points">
        {points}
    </ul>
</div>
"""

def _escape_markdown_to_html(md: str) -> str:
    """
    Very small markdown to HTML converter that only handles
    basic inline formatting (bold, italic, links) and escapes all other content.
    """
    # Escape everything first
    escaped = html.escape(md)

    # Convert Markdown link syntax [text](url) to <a href="url">text</a>
    import re
    def repl_link(match):
        text, url = match.group(1), match.group(2)
        return f'<a href="{html.escape(url)}">{text}</a>'

    escaped = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', repl_link, escaped)

    # Convert bold (**text**) and italic (*text*)
    escaped = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', escaped)
    escaped = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', escaped)

    return escaped

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a forum post from the given headline, content and discussion points.

    Parameters
    ----------
    headline : str
        Title of the forum post.
    content : str
        Main body text of the post. Markdown is allowed and will be converted to HTML.
    items : List[str]
        Discussion points or options. Each item is treated as a markdown string.

    Returns
    -------
    str
        A fully formatted, safe HTML forum post.

    Raises
    ------
    ValueError
        If any of the arguments are not strings or items is not a list of strings.
    """
    # Basic type validation
    if not isinstance(headline, str):
        raise ValueError("headline must be a string")
    if not isinstance(content, str):
        raise ValueError("content must be a string")
    if not isinstance(items, list) or not all(isinstance(i, str) for i in items):
        raise ValueError("items must be a list of strings")

    # Escape the headline
    safe_title = html.escape(headline)

    # Convert content from markdown to HTML safely
    safe_body = _escape_markdown_to_html(content)

    # Render each item as an <li> element
    rendered_items = []
    for idx, itm in enumerate(items):
        safe_itm = _escape_markdown_to_html(itm)
        rendered_items.append(f'<li id="point-{idx}">{safe_itm}</li>')

    safe_points = "\n".join(rendered_items)

    # Populate the template
    forum_post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )

    return forum_post_html.strip()