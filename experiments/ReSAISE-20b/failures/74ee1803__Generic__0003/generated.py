import html

# Pre‑defined HTML template for a blog post.
# The placeholders {title} and {body} will be replaced with the escaped content.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Formats and sanitizes a blog entry for safe HTML display.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The full content of the blog post.

    Returns
    -------
    str
        A fully rendered HTML string with user input escaped to prevent XSS.
    """
    # Escape any potentially dangerous characters in the user supplied strings
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Build the final HTML string using the template
    formatted_html = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_html