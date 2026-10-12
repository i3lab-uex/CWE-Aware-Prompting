# -*- coding: utf-8 -*-
"""
Utility for safely rendering a user‑submitted blog post.
"""

import html
from typing import Final

# Example template – replace with the actual format used in your project.
BLOG_FORMAT: Final[str] = """
<div class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</div>
"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Sanitize and format a blog post for safe display.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The main body content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML ready for rendering.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError(f"headline must be a string, got {type(headline).__name__}")
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    # Escape user input to prevent XSS attacks.
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Use the template to construct the final HTML.
    formatted = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted.strip()