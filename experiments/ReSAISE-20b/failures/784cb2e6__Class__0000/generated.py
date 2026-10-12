import html
from typing import List

# Predefined template for the forum post. The placeholders are:
#   {header}  - The title of the post
#   {body}    - The main body content
#   {options} - The unordered list of options/topics
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<div>{body}</div>
<ul>
{options}
</ul>
"""

def _sanitize_markdown(text: str) -> str:
    """
    Very lightweight sanitization of markdown text for safe rendering.
    Escapes HTML special characters and removes potential script tags.
    """
    # Escape all HTML entities
    escaped = html.escape(text)

    # Remove any remaining angle brackets that could form tags
    cleaned = escaped.replace("<", "&lt;").replace(">", "&gt;")
    return cleaned

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a sanitized forum post with a header, body, and unordered list of topics.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content or body of the forum post.
    topics : list[str]
        A collection of user-provided options or discussion points in markdown format.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post.
    """
    # Sanitize title, body, and each topic
    safe_title = _sanitize_markdown(title)
    safe_body = _sanitize_markdown(body)

    # Build the <li> elements for each topic
    list_items = []
    for t in topics:
        safe_topic = _sanitize_markdown(t)
        list_items.append(f"  <li>{safe_topic}</li>")
    options_html = "\n".join(list_items)

    # Fill the template
    formatted_post = FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=options_html
    )
    return formatted_post.strip()