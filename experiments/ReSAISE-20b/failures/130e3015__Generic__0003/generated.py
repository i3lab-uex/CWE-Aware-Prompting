import html

# Pre‑defined HTML template for a blog post.
# The placeholders {title} and {body} will be replaced with the sanitized content.
BLOG_FORMAT: str = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Formats a blog post for safe display on a webpage.

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

    Notes
    -----
    * The function uses ``html.escape`` to escape any characters that could form
      malicious HTML or JavaScript when rendered in a browser.
    * The resulting string is safe to embed directly into an HTML document
      without further escaping.
    """
    # Sanitize title and body to prevent XSS attacks.
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Insert sanitized content into the template.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return formatted_post