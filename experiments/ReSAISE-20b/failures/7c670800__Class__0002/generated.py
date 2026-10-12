# -*- coding: utf-8 -*-
"""
Utility to safely render a blog entry for display on a webpage.
"""

from __future__ import annotations

import html
from typing import Final

# Predefined format string for a blog entry.
# The placeholders are {title} and {body}.
BLOG_FORMAT: Final[str] = """
<article class="blog-entry">
    <h2>{title}</h2>
    <div class="content">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Return a sanitized and formatted HTML snippet for a blog entry.

    Parameters
    ----------
    heading : str
        The title of the blog post. It may contain user input.
    content : str
        The main body text of the blog post. It may contain user input.

    Returns
    -------
    str
        A string containing a fully escaped and formatted HTML block ready for
        safe rendering in the browser.

    Notes
    -----
    * The function uses :func:`html.escape` to neutralize any HTML or
      JavaScript that might be injected by a malicious user, protecting against
      CWE-74 (Injection via special characters).
    * The function does not perform any additional context‑sensitive
      sanitization (e.g., CSS or URL filtering) because the template only
      contains plain text content.
    """
    # Escape user supplied input to prevent XSS or other injection attacks.
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(content, quote=True)

    # Format the final output using the predefined template.
    formatted_entry = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_entry