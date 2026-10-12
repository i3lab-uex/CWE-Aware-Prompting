# -*- coding: utf-8 -*-

"""
A helper to safely render a blog entry into an HTML template.
"""

import html

# Pre‑defined template for the blog post
BLOG_FORMAT: str = """
<div class="blog-post">
    <h1>{headline}</h1>
    <div class="content">{text}</div>
</div>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Formats a blog entry using the BLOG_FORMAT template.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The full body of the blog post.

    Returns
    -------
    str
        A safe, HTML‑escaped string ready for insertion into a webpage.

    Notes
    -----
    - The function uses :func:`html.escape` to neutralize any characters that could
      otherwise break the HTML structure or introduce script injection.
    - It handles ``None`` values by treating them as empty strings, avoiding
      TypeErrors during formatting.
    """
    # Convert None to empty string for robustness
    if headline is None:
        headline = ""
    if text is None:
        text = ""

    # Escape user input to avoid XSS and malformed HTML
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Insert escaped values into the template
    formatted_entry = BLOG_FORMAT.format(headline=safe_headline, text=safe_text)

    return formatted_entry