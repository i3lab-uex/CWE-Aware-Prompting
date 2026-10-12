import html

# Predefined template for blog posts.
# The placeholders {title} and {body} will be replaced with the sanitized values.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

def publish_blog_article(subject: str, description: str) -> str:
    """
    Sanitize and format a user‑submitted blog post for safe display.

    Parameters
    ----------
    subject : str
        The heading/title of the blog post.
    description : str
        The main text content/body of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post,
        ready for safe rendering in an HTML page.

    Notes
    -----
    * Uses :func:`html.escape` to neutralize any characters that could be
      interpreted as HTML or JavaScript, protecting against XSS attacks.
    * The function does not perform any database operations; it only
      prepares the content for display.
    """
    # Sanitize inputs to prevent XSS and other injection attacks
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(description, quote=True)

    # Format the sanitized content into the predefined blog template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post