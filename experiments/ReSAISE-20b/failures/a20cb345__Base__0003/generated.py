import html

# Example template with placeholders for title and body.
BLOG_FORMAT = """
<article>
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>
"""

def publish_blog_article(subject: str, description: str) -> str:
    """
    Sanitize and format a blog article for safe display.

    Parameters
    ----------
    subject : str
        The heading of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post, ready for safe display.

    Raises
    ------
    ValueError
        If either argument is not a string.
    """
    if not isinstance(subject, str) or not isinstance(description, str):
        raise ValueError("Both subject and description must be strings.")

    # Escape all user-supplied content to neutralize XSS.
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(description, quote=True)

    # Use the predefined format string.
    formatted_article = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return formatted_article