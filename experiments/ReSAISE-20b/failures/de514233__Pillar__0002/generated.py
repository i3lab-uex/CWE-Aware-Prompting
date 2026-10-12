import html

# A simple HTML template for a blog post.  The placeholders are marked with {title}
# and {body} so they can be safely substituted.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Return a sanitized and formatted blog post ready for display.

    Parameters
    ----------
    headline : str
        The heading of the blog post.
    text : str
        The main body content of the blog post.

    Returns
    -------
    str
        A string containing a complete HTML snippet with the title and body safely escaped.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Escape any user supplied content to prevent XSS attacks.
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Format the sanitized content into the predefined template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)