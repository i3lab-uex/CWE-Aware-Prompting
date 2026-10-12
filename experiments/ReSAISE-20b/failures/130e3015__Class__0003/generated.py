import html

# Pre‑defined HTML template for blog posts.
BLOG_FORMAT = """
<article class="blog-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="content">
        {body}
    </section>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Safely format a blog post for display.

    Parameters
    ----------
    post_title : str
        The headline or title of the blog post.
    post_body : str
        The full text content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string ready for rendering.
    """
    # Escape special HTML characters to prevent XSS or injection attacks
    safe_title = html.escape(post_title, quote=True)
    safe_body  = html.escape(post_body, quote=True)

    # Insert the escaped values into the template
    formatted = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted