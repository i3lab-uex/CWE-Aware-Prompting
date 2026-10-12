# -*- coding: utf-8 -*-
"""
Utility module for rendering blog posts safely.
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

def display_blog(heading: str, description: str) -> str:
    """
    Render a blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized and HTML-formatted string ready for embedding in a webpage.

    Notes
    -----
    - All user-provided text is escaped to prevent XSS and other injection attacks.
    - The function uses a fixed template (BLOG_FORMAT) to ensure the output remains
      well-formed and consistent, mitigating CWE‑707 concerns about malformed data.
    """
    # Escape special HTML characters in both heading and description
    safe_heading = html.escape(heading, quote=True)
    safe_description = html.escape(description, quote=True)

    # Format the sanitized content into the predefined HTML structure
    rendered = BLOG_FORMAT.format(title=safe_heading, body=safe_description)

    return rendered.strip()