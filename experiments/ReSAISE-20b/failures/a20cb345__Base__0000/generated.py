import html

# Predefined template for blog posts.
# Example: "<h1>{title}</h1><p>{body}</p>"
BLOG_FORMAT = """<article>
  <header><h1>{title}</h1></header>
  <section>{body}</section>
</article>"""

def publish_blog_article(subject: str, description: str) -> str:
    """
    Safely formats a user-submitted blog post for display on a web page.

    Parameters
    ----------
    subject : str
        The title of the blog post.
    description : str
        The main body text of the blog post.

    Returns
    -------
    str
        A sanitized and formatted HTML snippet ready for safe display.
    """
    # Escape any HTML special characters to prevent XSS
    escaped_title = html.escape(subject, quote=True)
    escaped_body = html.escape(description, quote=True)

    # Format using the predefined template
    formatted_post = BLOG_FORMAT.format(title=escaped_title, body=escaped_body)

    return formatted_post