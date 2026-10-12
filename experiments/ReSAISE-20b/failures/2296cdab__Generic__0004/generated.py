# -*- coding: utf-8 -*-
"""
Utility to format user‑submitted blog entries for safe web display.
"""

import html
from typing import Final

# Predefined HTML structure with placeholders for title and body.
BLOG_FORMAT: Final[str] = """
<article class="blog-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="content">
        {body}
    </section>
</article>
"""


def format_blog_entry(headline: str, content: str) -> str:
    """
    Prepare a blog post for display by escaping HTML special characters
    and inserting the sanitized headline and content into a predefined
    template.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A fully rendered HTML string ready for safe presentation on the webpage.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError(f"headline must be a string, got {type(headline).__name__}")
    if not isinstance(content, str):
        raise TypeError(f"content must be a string, got {type(content).__name__}")

    # Escape HTML special characters to prevent XSS.
    safe_headline = html.escape(headline, quote=True)
    # Preserve line breaks in the body by converting newlines to <br> tags.
    safe_content = html.escape(content, quote=True).replace("\n", "<br>\n")

    return BLOG_FORMAT.format(title=safe_headline, body=safe_content)