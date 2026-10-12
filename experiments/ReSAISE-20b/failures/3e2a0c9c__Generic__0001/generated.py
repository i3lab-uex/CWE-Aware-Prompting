import html
from typing import List

# A simple, reusable HTML template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {discussion}
</div>
"""

def _escape_markdown_to_html(text: str) -> str:
    """
    Very small helper to escape text that might contain Markdown.
    Since we are rendering plain HTML, we simply escape HTML special
    characters. If Markdown parsing is needed in the future, this
    function can be replaced by a proper parser.
    """
    return html.escape(text)

def build_post_html(topic_title: str,
                    body_text: str,
                    list_items: List[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body or content of the forum post.
    list_items : List[str]
        A collection of discussion points in Markdown format.

    Returns
    -------
    str
        Fully formatted and sanitized HTML representation of the forum post.
    """
    # Sanitize title and body
    safe_title = _escape_markdown_to_html(topic_title)
    safe_body = _escape_markdown_to_html(body_text)

    # Build the unordered list for discussion points
    if list_items:
        safe_list_items = [
            f"<li>{_escape_markdown_to_html(item)}</li>"
            for item in list_items
        ]
        discussion_section = f"<ul>{''.join(safe_list_items)}</ul>"
    else:
        discussion_section = ""

    # Populate the template
    html_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        discussion=discussion_section
    )
    return html_post.strip()