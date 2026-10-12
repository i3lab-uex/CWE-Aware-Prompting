#!/usr/bin/env python3
"""
Utility for generating a safe, well‑formed forum post.

The module defines `create_forum_post`, which builds an HTML fragment
containing a header, body text and a list of discussion topics.
All user supplied content is escaped to prevent XSS or markup injection,
addressing CWE‑707 (Improper Neutralization of Structured Data).

Author: ChatGPT
"""

from __future__ import annotations

import html
from typing import List

# A simple template for the forum post.  The placeholders are
# ``{header}``, ``{message}`` and ``{options}``.  All parts are
# inserted as already‑escaped HTML fragments.
FORUM_POST_FORMAT: str = """
<div class="forum-post">
  <h2>{header}</h2>
  <div class="post-body">{message}</div>
  <ul class="discussion-topics">{options}</ul>
</div>
"""

def _escape_and_wrap_list_items(items: List[str]) -> str:
    """
    Escape each item and wrap it in an <li> element.

    Parameters
    ----------
    items : list[str]
        Raw markdown strings representing discussion topics.

    Returns
    -------
    str
        A concatenated string of <li> elements, each safely escaped.
    """
    list_items = []
    for item in items:
        # Strip surrounding whitespace to avoid accidental formatting.
        cleaned = item.strip()
        if not cleaned:
            continue  # Skip empty entries
        escaped = html.escape(cleaned, quote=True)
        list_items.append(f"<li>{escaped}</li>")
    return "\n".join(list_items)

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a sanitized HTML forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content or body text of the forum post.
    topics : list[str]
        A collection of user‑provided discussion points (markdown).

    Returns
    -------
    str
        A well‑formed, escaped HTML string ready for rendering.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Basic type validation – defensive programming to guard against
    # accidental misuse and to make debugging easier.
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(body, str):
        raise TypeError("body must be a string")
    if not isinstance(topics, list) or not all(isinstance(t, str) for t in topics):
        raise TypeError("topics must be a list of strings")

    # Escape the title and body to neutralize any embedded HTML or scripts.
    escaped_title = html.escape(title, quote=True)
    escaped_body = html.escape(body, quote=True)

    # Convert topics into a safe unordered list.
    options_html = _escape_and_wrap_list_items(topics)

    # Populate the template with the escaped fragments.
    post_html = FORUM_POST_FORMAT.format(
        header=escaped_title,
        message=escaped_body,
        options=options_html
    )

    # The returned string is safe for insertion into a page that expects
    # well‑formed HTML and does not allow unescaped user content.
    return post_html.strip()