# -*- coding: utf-8 -*-
"""
Blog post formatter with proper XSS protection.
"""

from html import escape

# Predefined HTML template for a blog post. The placeholders {title} and {body}
# will be replaced by the sanitized title and body strings.
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

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Sanitize and format a blog post for safe HTML rendering.

    Parameters
    ----------
    post_title : str
        The headline or title of the blog post. User-provided.
    post_body : str
        The full text content of the blog post. User-provided.

    Returns
    -------
    str
        A complete HTML string with the title and body safely escaped,
        suitable for inclusion in a web page.

    Notes
    -----
    * All user input is passed through html.escape, which converts special
      characters (e.g., <, >, &, ", ') into their HTML entity equivalents.
    * This approach protects against Cross‑Site Scripting (XSS) attacks
      (CWE-79) by ensuring that any embedded markup is rendered as plain text.
    * The function does not alter whitespace or line breaks in the body,
      preserving formatting.  If you need to convert newlines to <br> tags
      or wrap paragraphs, additional logic can be added here.
    """
    # Escape title and body to neutralize any HTML or script tags
    safe_title = escape(post_title, quote=True)
    safe_body = escape(post_body, quote=True)

    # Format the final HTML using the predefined template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)