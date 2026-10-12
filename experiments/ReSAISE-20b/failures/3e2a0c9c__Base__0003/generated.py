#!/usr/bin/env python3
"""
Utility for creating a sanitized HTML representation of a forum post.

The function `build_post_html` takes a title, body text, and an arbitrary list of
discussion points (supplied as markdown strings).  All user‑controlled input is
escaped to protect against Cross‑Site Scripting (CWE‑79) before being inserted
into the final HTML.

The output string uses a simple, predefined template `FORUM_POST_FORMAT`.
"""

from __future__ import annotations

import html
from typing import Iterable, List


# Predefined template with placeholders for title, body and discussion list.
FORUM_POST_FORMAT: str = """
<article class="forum-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="post-body">
        {body}
    </section>
    <footer class="discussion-points">
        <h2>Discussion Points</h2>
        {list_items}
    </footer>
</article>
"""


def _escape_markdown(md: str) -> str:
    """
    Escape a markdown string for safe inclusion in HTML.
    For this implementation we simply escape the entire string,
    which is sufficient for basic sanitization.  If richer
    markdown support is required, a dedicated parser should be used.
    """
    return html.escape(md)


def _build_list(items: Iterable[str]) -> str:
    """Convert an iterable of strings into a safe HTML unordered list."""
    escaped_items: List[str] = [_escape_markdown(item) for item in items]
    if not escaped_items:
        return "<p>No discussion points provided.</p>"
    list_html = ["<ul>"]
    for item in escaped_items:
        list_html.append(f"  <li>{item}</li>")
    list_html.append("</ul>")
    return "\n".join(list_html)


def build_post_html(topic_title: str, body_text: str, list_items: List[str]) -> str:
    """
    Construct a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body or content of the forum post.  It may contain user input.
    list_items : List[str]
        A collection of discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized HTML string ready for rendering.
    """
    if not isinstance(topic_title, str):
        raise TypeError("topic_title must be a string")
    if not isinstance(body_text, str):
        raise TypeError("body_text must be a string")
    if not isinstance(list_items, (list, tuple)):
        raise TypeError("list_items must be a list or tuple of strings")

    escaped_title = html.escape(topic_title)
    escaped_body = _escape_markdown(body_text)
    discussion_html = _build_list(list_items)

    return FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        list_items=discussion_html
    )