import html

# Predefined format for blog posts.
BLOG_FORMAT = """
<article>
  <header><h1>{title}</h1></header>
  <section><p>{body}</p></section>
</article>
"""

def publish_blog_article(subject: str, description: str) -> str:
    """
    Sanitize and format a user‑submitted blog post.

    Args:
        subject: The title of the blog post.
        description: The main text content of the blog post.

    Returns:
        A string containing the sanitized and formatted blog post,
        safe for rendering in an HTML page.

    Raises:
        ValueError: If either subject or description is empty.
    """
    if not subject or not description:
        raise ValueError("Subject and description must be non‑empty strings.")

    # Escape HTML to prevent XSS attacks.
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(description, quote=True)

    # Format the sanitized content using the template.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post