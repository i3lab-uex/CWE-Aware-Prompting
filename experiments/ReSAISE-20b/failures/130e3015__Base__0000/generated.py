import html

# Pre‑defined HTML template for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Format a blog post for safe display on a webpage.

    Parameters
    ----------
    post_title : str
        The headline or title of the blog post.
    post_body : str
        The full text content of the blog post.

    Returns
    -------
    str
        A sanitized and HTML‑formatted string ready to be injected into a page.
    """
    # Escape all user supplied content to prevent XSS attacks (CWE‑79).
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Insert the escaped content into the template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)