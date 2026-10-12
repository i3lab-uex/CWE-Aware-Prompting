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
    Sanitize and format a blog post for safe display on a webpage.

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
    """
    # Escape any HTML special characters to prevent XSS / injection attacks
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Insert the escaped content into the template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return formatted_post