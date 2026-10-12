import html

# Pre‑defined HTML template for a blog post.
# It contains two placeholders: {title} and {body}.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Format and safely display a user‑submitted blog entry.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The full body content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string ready to be injected into a webpage.
    """
    # Escape user input to neutralize XSS vectors.
    safe_title = html.escape(headline, quote=True)
    safe_body  = html.escape(text, quote=True)

    # Insert the escaped values into the template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)