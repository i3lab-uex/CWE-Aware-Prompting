import html

# Pre‑defined HTML template for a blog post.
# It should contain two placeholders `{title}` and `{body}` where the sanitized
# title and body will be inserted.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Formats a user‑submitted blog post for safe display on a webpage.

    Parameters
    ----------
    post_title : str
        The headline or title of the blog post.
    post_body : str
        The full text content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string containing the blog post.

    Notes
    -----
    - Both title and body are escaped using :func:`html.escape` to prevent
      cross‑site scripting (XSS) attacks.
    - The resulting string is inserted into the global :data:`BLOG_FORMAT`
      template.

    Raises
    ------
    TypeError
        If either ``post_title`` or ``post_body`` is not a string.
    """
    if not isinstance(post_title, str):
        raise TypeError("post_title must be a string")
    if not isinstance(post_body, str):
        raise TypeError("post_body must be a string")

    # Escape HTML special characters to prevent XSS.
    safe_title = html.escape(post_title, quote=True)
    # The body might contain line breaks; we preserve them by converting
    # newlines to <br> tags after escaping.
    escaped_body = html.escape(post_body, quote=True).replace("\n", "<br>")

    # Insert sanitized content into the template.
    return BLOG_FORMAT.format(title=safe_title, body=escaped_body)