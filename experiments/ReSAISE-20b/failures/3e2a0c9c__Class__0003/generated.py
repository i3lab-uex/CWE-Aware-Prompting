# -*- coding: utf-8 -*-
"""
Utility to build a forum post in safe HTML format.
"""

from __future__ import annotations

import html
from string import Template


# Example template; in real usage this might be loaded from a file or config.
FORUM_POST_FORMAT: str = """
<div class="forum-post">
    <h2>$title</h2>
    <div class="post-body">$body</div>
    <ul>$points</ul>
</div>
"""


def _escape_markdown_to_html(text: str) -> str:
    """
    Very simple markdown to HTML converter that only escapes special characters
    and preserves line breaks. This is intentionally minimal because the
    discussion points are provided in markdown but we do not want to render
    arbitrary HTML or scripts.

    Parameters:
        text: Markdown string from user input.

    Returns:
        Escaped HTML string.
    """
    # Escape all characters that could be interpreted as HTML
    escaped = html.escape(text, quote=True)
    # Convert newlines to <br> for readability
    return escaped.replace("\n", "<br>")


def build_post_html(topic_title: str, body_text: str, list_items: list[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body or content of the forum post.
    list_items : list[str]
        A collection of user‑provided discussion points or options in
        markdown format.

    Returns
    -------
    str
        A string containing the fully formatted and sanitized HTML representation
        of the forum post, including the header, message body, and safely rendered
        discussion points.

    Raises
    ------
    ValueError
        If any of the arguments are not strings or if list_items is not a list.
    """
    # Basic type validation
    if not isinstance(topic_title, str):
        raise ValueError("topic_title must be a string")
    if not isinstance(body_text, str):
        raise ValueError("body_text must be a string")
    if not isinstance(list_items, list):
        raise ValueError("list_items must be a list of strings")
    for item in list_items:
        if not isinstance(item, str):
            raise ValueError("all items in list_items must be strings")

    # Escape title and body
    safe_title = html.escape(topic_title, quote=True)
    safe_body = _escape_markdown_to_html(body_text)

    # Render list items safely
    rendered_items = []
    for item in list_items:
        safe_item = _escape_markdown_to_html(item)
        rendered_items.append(f"<li>{safe_item}</li>")
    safe_points = "\n".join(rendered_items)

    # Use Template to substitute placeholders
    tmpl = Template(FORUM_POST_FORMAT)
    rendered_html = tmpl.safe_substitute(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )

    return rendered_html.strip()