import html

# Predefined template for blog posts.
BLOG_FORMAT = """
<article>
    <h1>{title}</h1>
    <div class="content">
        {body}
    </div>
</article>
"""

def publish_blog_article(subject: str, description: str) -> str:
    """
    Sanitize and format a user‑submitted blog post for safe display on a web page.

    Parameters
    ----------
    subject : str
        The heading of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML ready for rendering.

    Raises
    ------
    ValueError
        If either `subject` or `description` is not a string.
    """
    if not isinstance(subject, str) or not isinstance(description, str):
        raise ValueError("Both subject and description must be strings.")

    # Escape special HTML characters to prevent XSS.
    safe_title = html.escape(subject, quote=True)
    # Escape the body and also convert newlines to <br> for readability.
    safe_body = html.escape(description, quote=True).replace("\n", "<br>")

    # Format the sanitized content into the predefined template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)