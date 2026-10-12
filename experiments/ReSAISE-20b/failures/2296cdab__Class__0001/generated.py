import html

# A simple HTML template for a blog post. The placeholders are used by str.format().
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
    Prepare a blog entry for safe web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized and HTML‑formatted string ready to be embedded in a web page.

    Notes
    -----
    * The function uses :func:`html.escape` to neutralise any characters that could
      otherwise be interpreted as HTML, preventing injection attacks (CWE‑74).
    * The returned string contains the supplied headline and content substituted
      into :data:`BLOG_FORMAT`.
    """
    # Ensure both arguments are strings; if not, convert them.
    headline = str(headline)
    content = str(content)

    # Escape special HTML characters to prevent injection.
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the final HTML using the template.
    formatted_post = BLOG_FORMAT.format(title=safe_headline, body=safe_content)

    return formatted_post