import html

# Predefined template for a blog post.  The placeholders are replaced with the escaped title
# and body when rendering the article.
BLOG_FORMAT = (
    "<article class=\"blog-post\">\n"
    "  <h1>{title}</h1>\n"
    "  <div class=\"post-body\">\n"
    "    {body}\n"
    "  </div>\n"
    "</article>"
)

def publish_blog_article(subject: str, description: str) -> str:
    """
    Render a user‑submitted blog post safely for display on a web page.

    Parameters
    ----------
    subject : str
        The title of the blog post.
    description : str
        The main body text of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post ready for safe display.
    """
    # Escape any HTML special characters to prevent injection attacks
    escaped_title = html.escape(subject, quote=True)
    escaped_body = html.escape(description, quote=True)

    # Construct the final output using a safe template
    return BLOG_FORMAT.format(title=escaped_title, body=escaped_body)