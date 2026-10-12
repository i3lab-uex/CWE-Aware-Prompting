# -*- coding: utf-8 -*-
"""
Utility for rendering a user‑generated blog post safely.
"""

import html
from typing import Final

# Template for displaying a blog post.  The placeholders are replaced with
# the escaped title and body.
BLOG_FORMAT: Final[str] = """
<div class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</div>
"""


def render_blog_post(title: str, body: str) -> str:
    """
    Render a blog post with the given title and body.

    The function sanitizes the input to avoid XSS attacks by escaping
    all HTML special characters.  It then injects the sanitized strings
    into a predefined template.

    Parameters
    ----------
    title : str
        The title of the blog post.  Empty titles are allowed but will be
        rendered as an empty <h1> element.
    body : str
        The main content of the blog post.  Empty bodies are allowed.

    Returns
    -------
    str
        The fully rendered blog post ready for safe inclusion in an HTML page.

    Raises
    ------
    TypeError
        If either `title` or `body` is not a string.
    """
    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")
    if not isinstance(body, str):
        raise TypeError(f"body must be a string, got {type(body).__name__}")

    # Escape user supplied content to prevent injection of malicious HTML.
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Render the template with sanitized values.
    rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return rendered.strip()