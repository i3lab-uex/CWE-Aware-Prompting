import html

# Template for the blog post. Use {title} and {body} as placeholders.
BLOG_FORMAT = (
    "<article class=\"blog-post\">\n"
    "  <h1>{title}</h1>\n"
    "  <div class=\"content\">{body}</div>\n"
    "</article>"
)

def publish_blog_article(subject: str, description: str) -> str:
    """
    Safely format a blog article for display.

    Parameters
    ----------
    subject : str
        The title of the blog post.
    description : str
        The main body content of the blog post.

    Returns
    -------
    str
        A sanitized and formatted HTML string ready for safe rendering.
    """
    # Escape any potentially dangerous characters to prevent XSS or injection attacks.
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(description, quote=True)

    # Format the sanitized strings into the predefined template.
    formatted_article = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_article