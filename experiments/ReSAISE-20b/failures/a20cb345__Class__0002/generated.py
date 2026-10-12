import html

# Predefined template for the blog post.  
# It uses `{title}` and `{body}` as placeholders.
BLOG_FORMAT = """
<article>
  <h1>{title}</h1>
  <section>{body}</section>
</article>
"""

def publish_blog_article(subject: str, description: str) -> str:
    """
    Return a sanitized and formatted blog post ready for safe display.

    Parameters
    ----------
    subject : str
        The heading of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post.
    """
    # Escape any HTML special characters to avoid injection (CWE‑74).
    safe_title = html.escape(subject, quote=True)
    safe_body  = html.escape(description, quote=True)

    # Render the final HTML using the template.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post