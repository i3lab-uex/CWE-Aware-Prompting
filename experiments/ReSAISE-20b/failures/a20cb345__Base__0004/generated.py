import html

# Predefined template for a blog post.  The placeholders will be replaced with the
# sanitized title and description.
BLOG_FORMAT = (
    "<article>\n"
    "  <h1>{title}</h1>\n"
    "  <div class=\"content\">\n{body}\n  </div>\n</article>"
)

def publish_blog_article(subject: str, description: str) -> str:
    """
    Return a sanitized and formatted blog post ready for safe display.

    Parameters
    ----------
    subject : str
        The heading of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post.
    """
    # Escape any HTML special characters to prevent XSS
    safe_title = html.escape(subject, quote=True)
    # Convert newlines to <br> tags so formatting is preserved in HTML
    safe_body = html.escape(description, quote=True).replace("\n", "<br>\n")

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)