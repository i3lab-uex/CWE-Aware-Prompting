import html

# Predefined template for formatting blog posts.
# It contains placeholders {title} and {body}.
BLOG_FORMAT = (
    "<article>\n"
    "  <h1>{title}</h1>\n"
    "  <div class=\"content\">\n"
    "    {body}\n"
    "  </div>\n"
    "</article>"
)

def publish_blog_article(subject: str, description: str) -> str:
    """
    Sanitize and format a blog post for safe display on a webpage.

    Parameters
    ----------
    subject : str
        The heading of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post,
        ready for safe display.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(subject, str):
        raise TypeError("subject must be a string")
    if not isinstance(description, str):
        raise TypeError("description must be a string")

    # Escape HTML special characters to prevent XSS attacks.
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(description, quote=True)

    # Insert the sanitized content into the template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)