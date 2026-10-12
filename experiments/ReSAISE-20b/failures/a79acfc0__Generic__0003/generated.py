import html

# Example template; adjust as needed for your application.
BLOG_FORMAT = """
<div class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</div>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user-generated blog post safely for web display.

    Parameters
    ----------
    title : str
        The title of the blog post.
    body : str
        The main content of the blog post.

    Returns
    -------
    str
        A sanitized HTML string with the title and body inserted into BLOG_FORMAT.

    Raises
    ------
    ValueError
        If either title or body is empty after stripping whitespace.
    """
    # Basic validation: ensure non-empty content
    if not title or not body:
        raise ValueError("Both title and body must be provided.")

    # Strip leading/trailing whitespace
    clean_title = title.strip()
    clean_body = body.strip()

    # Escape HTML special characters to prevent XSS
    escaped_title = html.escape(clean_title, quote=True)
    escaped_body = html.escape(clean_body, quote=True)

    # Insert into the template
    rendered_html = BLOG_FORMAT.format(title=escaped_title, body=escaped_body)

    return rendered_html