import html

# Pre‑defined HTML template for a blog post.
# The placeholders {title} and {body} will be replaced by the escaped values.
BLOG_FORMAT = """
<article class="blog-post">
    <h2>{title}</h2>
    <div class="content">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Format and safely render a user‑submitted blog entry.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The full body content of the blog post.

    Returns
    -------
    str
        A sanitized HTML string ready to be inserted into a webpage.

    Raises
    ------
    TypeError
        If either `headline` or `text` is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError(f"headline must be a string, got {type(headline).__name__}")
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    # Escape special HTML characters to prevent XSS.
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Replace placeholders in the template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)