#!/usr/bin/env python3
"""
Forum post generation with proper XSS protection.

The function `generate_forum_post` takes a header, message and a list of
markdown options and returns a sanitized HTML snippet that can safely be
included in a web page.

The implementation uses `html.escape` to neutralise any HTML or script
content that might be injected by a malicious user.  No further Markdown
processing is performed – the input is treated as plain text and rendered
inside <li> elements of an unordered list.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import html
from typing import Iterable, List


# Template used to render the forum post.
FORUM_POST_FORMAT: str = """
<h2>{header}</h2>
<p>{message}</p>
{options_html}
"""


def _escape_markdown(text: str) -> str:
    """
    Escape a string that may contain Markdown syntax so that it cannot
    break the surrounding HTML structure.

    Parameters
    ----------
    text : str
        Raw user input that may contain Markdown.

    Returns
    -------
    str
        The escaped string safe for inclusion inside HTML.
    """
    return html.escape(text, quote=True)


def generate_forum_post(
    header: str,
    message: str,
    options: Iterable[str] | None = None
) -> str:
    """
    Generate a sanitized forum post.

    Parameters
    ----------
    header : str
        The title of the post.
    message : str
        The body text of the post.
    options : Iterable[str] | None, optional
        A list of user‑submitted options (in Markdown format).  If `None`
        or empty, no <ul> element is rendered.

    Returns
    -------
    str
        The complete forum post as an HTML string, safe from XSS attacks.

    Raises
    ------
    TypeError
        If any argument is of an unexpected type.
    """
    if not isinstance(header, str):
        raise TypeError("header must be a string")
    if not isinstance(message, str):
        raise TypeError("message must be a string")

    # Sanitize header and message
    safe_header = _escape_markdown(header)
    safe_message = _escape_markdown(message)

    # Process options
    if options is None:
        options = []

    safe_options: List[str] = []
    for opt in options:
        if not isinstance(opt, str):
            raise TypeError("each option must be a string")
        safe_opt = _escape_markdown(opt)
        safe_options.append(f"<li>{safe_opt}</li>")

    if safe_options:
        options_html = "<ul>\n" + "\n".join(safe_options) + "\n</ul>"
    else:
        options_html = ""

    # Render the final post
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_html=options_html
    ).strip()