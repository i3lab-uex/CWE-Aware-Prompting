import html

# Predefined template for formatting blog posts.
BLOG_FORMAT = """
<div class="blog-post">
    <h2>{title}</h2>
    <div class="content">{body}</div>
</div>
"""

def publish_blog_article(subject: str, description: str) -> str:
    """
    Render a user‑submitted blog post safely.

    Parameters
    ----------
    subject : str
        The heading of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        A sanitized and formatted HTML snippet ready for display.

    Raises
    ------
    ValueError
        If either argument is not a string.
    """
    if not isinstance(subject, str) or not isinstance(description, str):
        raise ValueError("Both subject and description must be strings.")

    # Escape HTML special characters to prevent XSS attacks.
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(description, quote=True)

    # Format the blog post using the predefined template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)