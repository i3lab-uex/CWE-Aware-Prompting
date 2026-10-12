#!/usr/bin/env python3
"""
Utility to build a safe, structured forum post from user supplied content.
"""

from __future__ import annotations

import html
from typing import Iterable, List

# --------------------------------------------------------------------------- #
# Configuration: a simple HTML template used for all forum posts.
# The placeholders `{title}`, `{content}` and `{items}` will be replaced
# with the escaped user content.
#
# NOTE: The template is intentionally minimal to reduce the attack surface
# and avoid inadvertent injection of malicious markup.
FORUM_POST_FORMAT: str = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-content">{content}</div>
  {items}
</div>
"""

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _escape(text: str) -> str:
    """
    Escape a string for safe inclusion in HTML.
    Uses `html.escape` which escapes &, <, >, " and '.

    Parameters
    ----------
    text : str
        The raw user input.

    Returns
    -------
    str
        Escaped text safe for HTML rendering.
    """
    return html.escape(text, quote=True)

def _build_unordered_list(items: Iterable[str]) -> str:
    """
    Convert an iterable of strings into a safe HTML unordered list.

    Parameters
    ----------
    items : Iterable[str]
        Raw user supplied strings, possibly in Markdown format.

    Returns
    -------
    str
        A `<ul>` element containing each item as an escaped `<li>`.
    """
    if not items:
        return ""

    list_items: List[str] = []
    for item in items:
        # Escape each item to neutralize any embedded markup.
        escaped = _escape(str(item))
        list_items.append(f"<li>{escaped}</li>")

    return "<ul>\n" + "\n".join(list_items) + "\n</ul>"

# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a forum post from the given headline, content and discussion points.

    The function sanitizes all user inputs to prevent XSS or markup injection.
    It also guards against CWE-707 by ensuring the final output is well‑formed
    HTML and that all dynamic parts are properly escaped.

    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary body text of the post. May contain newlines.
    items : List[str]
        Discussion points or options in Markdown format.

    Returns
    -------
    str
        A fully formatted, safe HTML forum post ready for rendering.

    Raises
    ------
    ValueError
        If any of the arguments is not a string or list of strings.
    """
    # Basic type validation
    if not isinstance(headline, str):
        raise ValueError("headline must be a string")
    if not isinstance(content, str):
        raise ValueError("content must be a string")
    if not isinstance(items, (list, tuple)):
        raise ValueError("items must be a list or tuple of strings")

    # Escape headline and content
    safe_headline = _escape(headline)
    safe_content = _escape(content).replace("\n", "<br>")  # Preserve line breaks

    # Build the discussion points list
    safe_items_html = _build_unordered_list(items)

    # Format the final post
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_headline,
        content=safe_content,
        items=safe_items_html
    )

    return formatted_post.strip()

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_headline = "Welcome to the Forum!"
    sample_content = (
        "Hello everyone,\n"
        "Feel free to share your thoughts below.\n"
        "<script>alert('xss');</script>"
    )
    sample_items = [
        "Option 1: **Bold** text",
        "Option 2: <img src=x onerror=alert(1)>",
        "Option 3: [Link](http://example.com)",
    ]

    post = build_forum_post(sample_headline, sample_content, sample_items)
    print(post)