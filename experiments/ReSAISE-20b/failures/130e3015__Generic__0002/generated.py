import html

# Example blog format template with placeholders for title and body.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Formats a blog post for safe HTML display.

    Parameters
    ----------
    post_title : str
        The headline or title of the blog post.
    post_body : str
        The full text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(post_title, str):
        raise TypeError(f"post_title must be a string, got {type(post_title).__name__}")
    if not isinstance(post_body, str):
        raise TypeError(f"post_body must be a string, got {type(post_body).__name__}")

    # Escape any HTML special characters to prevent XSS
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)

    # Insert escaped content into the template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post