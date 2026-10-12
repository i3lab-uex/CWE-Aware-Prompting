import html

# Predefined template for a blog post.
BLOG_FORMAT = "<article>\n  <h1>{title}</h1>\n  <div class=\"content\">{body}</div>\n</article>"

def publish_blog_article(subject: str, description: str) -> str:
    """
    Render a user‑submitted blog post safely for display.

    Parameters
    ----------
    subject : str
        The title of the blog post.
    description : str
        The main body content of the blog post.

    Returns
    -------
    str
        A sanitized, formatted HTML string ready for safe rendering.
    """
    # Escape any characters that could be interpreted as markup or script
    safe_title = html.escape(subject, quote=True)
    safe_body  = html.escape(description, quote=True)

    # Insert the sanitized content into the template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post