import html
from typing import List

# Predefined template for forum posts.
# Placeholders:
#   {header} – the title of the post
#   {body}   – the main content
#   {options}– an unordered list of discussion topics
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<div class="post-body">
    {body}
</div>
{options}
"""

def _markdown_to_html(text: str) -> str:
    """
    Very small markdown-to-HTML converter for a subset of markdown.
    It escapes all HTML characters and converts simple list syntax
    (lines starting with `-` or `*`) into <li> elements.
    """
    # Escape all HTML to avoid injection
    escaped = html.escape(text)

    lines = escaped.splitlines()
    list_items: List[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            item_text = stripped[2:].strip()
            list_items.append(f"<li>{item_text}</li>")
        else:
            # Preserve paragraphs
            list_items.append(f"<p>{stripped}</p>")
    return "\n".join(list_items)

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a forum post with the given title, body and discussion topics.

    Parameters
    ----------
    title : str
        The subject line of the post.
    body : str
        Main content. May contain markdown, which will be escaped for safety.
    topics : list[str]
        Discussion points. Each string may contain markdown; only a very small
        subset (list items) is converted to HTML.

    Returns
    -------
    str
        A sanitized, formatted forum post ready for rendering in a browser.
    """
    # Sanitize title
    safe_title = html.escape(title)

    # Convert body from markdown to HTML, escaping all user content
    safe_body = _markdown_to_html(body)

    # Convert topics to an unordered list.
    if not topics:
        options_html = ""
    else:
        # Convert each topic string to HTML list item
        items = []
        for topic in topics:
            # Each topic may contain markdown; convert it
            item_html = _markdown_to_html(topic).strip()
            items.append(f"<li>{item_html}</li>")
        options_html = f"<ul>\n{''.join(items)}\n</ul>"

    # Populate the template
    post = FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=options_html
    )
    return post.strip()