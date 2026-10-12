# -*- coding: utf-8 -*-
"""
Utility to safely format and display user‑submitted blog posts.

The module uses the standard library only, ensuring no external
dependencies and mitigating common XSS vulnerabilities by escaping all
user input before insertion into the HTML template.
"""

import html

# Define a simple but flexible blog post template. The placeholders
# use the same names as the function arguments for readability.
BLOG_FORMAT: str = """
<article class="blog-post">
    <h2>{headline}</h2>
    <div class="post-body">{text}</div>
</article>
"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Return a sanitized and formatted HTML string for a blog post.

    Parameters
    ----------
    headline : str
        The title of the blog post. It will be escaped to avoid
        rendering any HTML or script content.
    text : str
        The main body of the post. All markup is escaped to ensure safe display.

    Returns
    -------
    str
        A fully formatted HTML snippet ready for insertion into a page.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError(f"headline must be a string, got {type(headline).__name__}")
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    # Escape user-provided content to prevent XSS attacks.
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Format the final HTML using the predefined template.
    return BLOG_FORMAT.format(headline=safe_headline, text=safe_text).strip()