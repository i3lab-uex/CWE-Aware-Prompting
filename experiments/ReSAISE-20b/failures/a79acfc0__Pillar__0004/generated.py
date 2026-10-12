import html

# Template for rendering a blog post on the web page.
BLOG_FORMAT = """
<div class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</div>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user-generated blog post safely for display on a web page.

    Parameters
    ----------
    title : str
        The title of the blog post.
    body : str
        The main content/body of the blog post.

    Returns
    -------
    str
        A sanitized HTML string that can be safely inserted into a page.
    
    Raises
    ------
    TypeError
        If either title or body is not a string.
    """
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(body, str):
        raise TypeError("body must be a string")

    # Escape user input to prevent XSS and ensure well‑formed HTML
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Insert the sanitized values into the template
    rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return rendered.strip()