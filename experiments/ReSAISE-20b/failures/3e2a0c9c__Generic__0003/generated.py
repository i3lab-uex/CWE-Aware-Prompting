import html
from typing import List

# Example template used by the forum system.
FORUM_POST_FORMAT: str = (
    "<article class='forum-post'>"
    "  <header><h1>{title}</h1></header>"
    "  <section class='post-body'>{body}</section>"
    "  <footer><ul>{items}</ul></footer>"
    "</article>"
)


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
        A collection of user‑provided discussion points or options in markdown
        format. Each item will be rendered as an <li> element.

    Returns
    -------
    str
        A string containing the fully formatted and sanitized HTML representation
        of the forum post, including the header, message body, and safely rendered
        discussion points.

    Raises
    ------
    ValueError
        If any of the arguments are not of the expected type.
    """
    if not isinstance(topic_title, str):
        raise ValueError("topic_title must be a string")
    if not isinstance(body_text, str):
        raise ValueError("body_text must be a string")
    if not isinstance(list_items, list) or not all(isinstance(item, str) for item in list_items):
        raise ValueError("list_items must be a list of strings")

    # Escape user supplied text to prevent XSS attacks
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Render each list item safely
    rendered_items = []
    for item in list_items:
        escaped_item = html.escape(item, quote=True)
        rendered_items.append(f"<li>{escaped_item}</li>")
    items_html = "\n".join(rendered_items)

    # Insert into the template
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        items=items_html
    )
    return post_html