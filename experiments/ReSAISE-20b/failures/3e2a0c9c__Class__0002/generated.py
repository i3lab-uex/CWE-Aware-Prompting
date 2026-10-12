import html
from typing import List

# Example forum post template. Replace or modify as needed.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {list_section}
</div>
"""

def build_post_html(topic_title: str, body_text: str, list_items: List[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body or content of the forum post.
    list_items : List[str]
        A collection of user‑provided discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML representation of the forum post.

    Raises
    ------
    ValueError
        If any argument is not of the expected type.
    """
    # Validate input types
    if not isinstance(topic_title, str):
        raise ValueError("topic_title must be a string")
    if not isinstance(body_text, str):
        raise ValueError("body_text must be a string")
    if not isinstance(list_items, list) or not all(isinstance(i, str) for i in list_items):
        raise ValueError("list_items must be a list of strings")

    # Escape user supplied content to prevent HTML injection
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Build the unordered list section
    if list_items:
        safe_list_items = "".join(
            f"<li>{html.escape(item, quote=True)}</li>" for item in list_items
        )
        list_section = f"<ul>{safe_list_items}</ul>"
    else:
        list_section = ""

    # Format the final HTML
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        list_section=list_section
    )