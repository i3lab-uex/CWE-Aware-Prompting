import html

# Predefined template for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>
"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Render a user‑submitted blog post safely for display in HTML.

    Parameters
    ----------
    headline : str
        The title of the blog post.  Must not be empty.
    text : str
        The body content of the blog post.  Must not be empty.

    Returns
    -------
    str
        A sanitized HTML string containing the blog post.

    Raises
    ------
    ValueError
        If either `headline` or `text` is empty.
    """
    if not headline:
        raise ValueError("headline must be a non‑empty string")
    if not text:
        raise ValueError("text must be a non‑empty string")

    # Escape user input to prevent XSS (CWE‑79)
    safe_title = html.escape(headline, quote=True)
    safe_body  = html.escape(text, quote=True)

    # Return the formatted HTML
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)