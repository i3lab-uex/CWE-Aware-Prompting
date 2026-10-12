# -*- coding: utf-8 -*-
"""
Safe rendering of user‑submitted blog posts.

This module defines a single function, `render_article_page`, which accepts
a headline and body text for a blog post and returns an HTML string that is
safe to embed in a web page.  The function uses the standard library's
`html.escape` to neutralise any potentially malicious content, protecting
against cross‑site scripting (CWE‑79).

Author: OpenAI ChatGPT
"""

import html

# Predefined HTML template for a blog post.
# The placeholders `{title}` and `{body}` will be replaced by escaped
# values supplied by the caller.
BLOG_FORMAT: str = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def render_article_page(headline: str, content: str) -> str:
    """
    Return a sanitized HTML representation of a blog post.

    Parameters
    ----------
    headline : str
        The title or headline of the blog post.
    content : str
        The full body text of the blog post.

    Returns
    -------
    str
        An HTML string that can be safely embedded in a web page.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")

    # Escape any HTML special characters to prevent XSS.
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Insert the escaped values into the template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)