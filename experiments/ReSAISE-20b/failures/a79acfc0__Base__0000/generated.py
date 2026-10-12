import html

# Template for rendering a blog post in HTML
BLOG_FORMAT = """
<div class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</div>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user‑generated blog post safely for display on a web page.

    Parameters
    ----------
    title : str
        The blog post title entered by the user.
    body : str
        The main content of the blog post entered by the user.

    Returns
    -------
    str
        An HTML string containing the sanitized title and body, formatted with BLOG_FORMAT.
    """
    # Escape all user input to prevent XSS (CWE‑79)
    safe_title = html.escape(title, quote=True)
    safe_body  = html.escape(body, quote=True)

    # Insert the escaped values into the template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)