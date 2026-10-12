import html

# Predefined HTML structure for a blog post.
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
    Prepare a user‑submitted blog entry for web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string ready for rendering on a web page.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str) or not isinstance(content, str):
        raise TypeError("Both headline and content must be strings")

    # Escape all user input to neutralize potential XSS vectors.
    safe_headline = html.escape(headline, quote=True)
    # Preserve paragraph breaks by converting newlines to <br> tags after escaping.
    safe_content = html.escape(content, quote=True).replace("\n", "<br>\n")

    return BLOG_FORMAT.format(title=safe_headline, body=safe_content)