import html

# Template for rendering a blog post; placeholders: {title}, {body}
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user-generated blog post safely.

    Parameters
    ----------
    title : str
        The title of the blog post.
    body : str
        The main content of the blog post.

    Returns
    -------
    str
        A sanitized HTML string ready for display in a web page.

    Raises
    ------
    ValueError
        If either title or body is empty after stripping whitespace.
    """
    if not isinstance(title, str) or not isinstance(body, str):
        raise TypeError("Title and body must be strings")

    # Strip leading/trailing whitespace
    title = title.strip()
    body = body.strip()

    if not title:
        raise ValueError("Title cannot be empty")
    if not body:
        raise ValueError("Body cannot be empty")

    # Escape HTML special characters to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Use the provided format template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)