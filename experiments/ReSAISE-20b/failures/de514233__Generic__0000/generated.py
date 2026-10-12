# -*- coding: utf-8 -*-
"""
Utility to safely render a blog post for display.
"""

import html
from typing import Final

# Example format: you can adjust the template to match your HTML structure.
BLOG_FORMAT: Final[str] = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""


def show_blog_post(headline: str, text: str) -> str:
    """
    Return a sanitized and formatted blog post ready for safe display.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The main content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML snippet.
    """
    # Escape special characters to prevent XSS attacks
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Format the sanitized content into the predefined template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)