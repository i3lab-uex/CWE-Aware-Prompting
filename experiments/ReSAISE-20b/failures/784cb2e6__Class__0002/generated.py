# -*- coding: utf-8 -*-
"""
Utility for constructing safe, formatted forum posts.

The implementation protects against HTML injection by escaping all user‑supplied
content before inserting it into the output template.  The options are rendered
as an HTML unordered list (<ul>) to provide a clear visual structure.
"""

from html import escape
from typing import List

# Predefined template for forum posts.  Placeholders:
#   {header}   – the escaped title
#   {message}  – the escaped body
#   {options}  – the rendered <ul> list of options
FORUM_POST_FORMAT: str = (
    "<h1>{header}</h1>\n"
    "<div class=\"post-body\">{message}</div>\n"
    "<h2>Discussion Topics</h2>\n"
    "<ul>{options}</ul>"
)

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a safe, formatted forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content or body of the forum post.
    topics : list[str]
        A collection of discussion points or options in markdown format.

    Returns
    -------
    str
        The sanitized and formatted forum post, including the header,
        message body, and options rendered as an HTML unordered list.

    Raises
    ------
    TypeError
        If any of the arguments are not of the expected type.
    """
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(body, str):
        raise TypeError("body must be a string")
    if not isinstance(topics, list) or not all(isinstance(t, str) for t in topics):
        raise TypeError("topics must be a list of strings")

    # Escape user‑supplied content to neutralize special HTML characters
    safe_title = escape(title, quote=True)
    safe_body = escape(body, quote=True)

    # Render each topic as a list item; ensure each is safely escaped
    safe_topics = "".join(f"<li>{escape(topic, quote=True)}</li>" for topic in topics)

    # Format the final post
    forum_post = FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=safe_topics
    )

    return forum_post