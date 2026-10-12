import html

# Template for rendering a blog post.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user‑generated blog post safely.

    Parameters
    ----------
    title : str
        The title of the blog post.
    body : str
        The main content of the blog post.

    Returns
    -------
    str
        A sanitized HTML string ready for display.
    """
    # Escape user input to prevent XSS attacks
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Render the template with sanitized values
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)