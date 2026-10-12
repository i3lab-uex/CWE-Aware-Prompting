import html

# Predefined HTML structure for a blog post.
BLOG_FORMAT = (
    '<article class="blog-post">'
    '  <h1>{title}</h1>'
    '  <div class="post-content">{body}</div>'
    '</article>'
)

def format_blog_entry(headline: str, content: str) -> str:
    """
    Sanitize and embed a blog headline and its content into an HTML template.

    Parameters
    ----------
    headline : str
        The main heading of the blog post.
    content : str
        The full text of the blog post.

    Returns
    -------
    str
        A complete HTML snippet ready for display on a webpage.

    Raises
    ------
    TypeError
        If either ``headline`` or ``content`` is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")

    # Escape any HTML special characters to prevent injection attacks.
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    return BLOG_FORMAT.format(title=safe_headline, body=safe_content)