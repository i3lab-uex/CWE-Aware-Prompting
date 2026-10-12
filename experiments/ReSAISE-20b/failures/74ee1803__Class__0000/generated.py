import html

# Pre‑defined HTML template for a blog post.
# The placeholders {headline} and {text} will be replaced with escaped user input.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{headline}</h1>
    <div class="post-body">{text}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Format and sanitize a user‑submitted blog post for safe HTML display.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The full body content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized, HTML‑formatted blog post.

    Notes
    -----
    * Uses :func:`html.escape` to neutralise any special characters that could
      otherwise break the HTML structure or enable injection attacks.
    * The function assumes ``BLOG_FORMAT`` contains exactly two placeholders
      named ``{headline}`` and ``{text}``.
    """
    # Escape user input to prevent XSS or HTML injection.
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Format the sanitized values into the template.
    formatted_post = BLOG_FORMAT.format(headline=safe_headline, text=safe_text)

    return formatted_post