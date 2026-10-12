# -*- coding: utf-8 -*-

"""
Utility for safely rendering a user‑submitted blog entry.
"""

import html
from typing import Final

# Predefined template – uses {title} and {body} placeholders.
BLOG_FORMAT: Final[str] = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Render a blog entry safely for HTML output.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main text body of the blog post.

    Returns
    -------
    str
        A fully formatted, HTML‑escaped string ready for display.

    Notes
    -----
    * All user input is escaped with :func:`html.escape` to prevent XSS.
    * The function does **not** perform any additional sanitisation beyond
      escaping; if richer sanitisation is required (e.g. stripping tags),
      a dedicated library such as `bleach` should be used.
    """
    # Escape user‑supplied data to neutralise HTML special characters.
    safe_title = html.escape(heading, quote=True)
    safe_body  = html.escape(content, quote=True)

    # Format the blog post with the sanitized values.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post