import html

# Template for a blog post; placeholders are {title} and {body}
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user-generated blog post safely for display in a web page.

    Parameters
    ----------
    title : str
        The title of the blog post.
    body : str
        The main content of the blog post.

    Returns
    -------
    str
        A fully escaped HTML snippet containing the title and body.
    """
    # Escape user-provided input to prevent XSS (CWE-79)
    safe_title = html.escape(title, quote=True)
    safe_body  = html.escape(body, quote=True)

    # Return the formatted HTML
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)