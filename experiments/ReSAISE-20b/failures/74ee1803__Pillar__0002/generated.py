# -*- coding: utf-8 -*-
"""
Blog entry renderer with basic XSS protection.
"""

import html
from typing import Final

# Example template; in a real project this would come from a config or
# template engine.
BLOG_FORMAT: Final[str] = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Format a blog entry for safe display on a webpage.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The main body of the blog post.

    Returns
    -------
    str
        A string containing the HTML representation of the post,
        with all user-supplied content properly escaped to avoid
        XSS and other injection attacks.

    Notes
    -----
    * The function uses :func:`html.escape` to neutralise any HTML
      entities that could be interpreted by the browser.
    * It also removes potential script tags that might slip through
      by escaping them.  The template does not use any `unsafe` rendering
      features, so the result is safe to inject directly into a page.
    """
    # Validate input types
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Escape user input to neutralise HTML special characters
    safe_title = html.escape(headline, quote=True)
    safe_body  = html.escape(text, quote=True)

    # Render the final HTML
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)