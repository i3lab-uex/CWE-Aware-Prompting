#!/usr/bin/env python3
"""
Blog post formatter.

The function `format_blog_entry` takes a headline and the body of a blog
post, sanitises them for safe HTML rendering and injects them into a
pre‑defined template.

The implementation follows the following security principles:

* Input validation – only strings are accepted.
* Output escaping – all HTML special characters are escaped to avoid
  injection of malicious markup or scripts.
* Structured output – the resulting string always contains the same
  well‑formed HTML skeleton, protecting against malformed or partial
  responses (CWE‑707).

"""

import html

# Predefined HTML structure with placeholders for title and body
BLOG_FORMAT = """
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
    Prepare a blog post for web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string ready for rendering.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")

    # Escape HTML special characters to prevent injection attacks.
    safe_title = html.escape(headline, quote=True)
    # For the body we escape but also preserve line breaks as <br>.
    escaped_body = html.escape(content, quote=True).replace("\n", "<br>\n")

    # Insert the sanitized parts into the template.
    formatted = BLOG_FORMAT.format(title=safe_title, body=escaped_body)

    return formatted.strip()