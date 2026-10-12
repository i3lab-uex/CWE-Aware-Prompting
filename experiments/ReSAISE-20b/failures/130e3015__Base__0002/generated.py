import html

# Predefined HTML template for a blog post.  The placeholders `{title}` and `{body}`
# will be replaced by the sanitized title and body.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Sanitize and format a blog post for safe HTML rendering.

    Parameters
    ----------
    post_title : str
        The headline or title of the blog post.
    post_body : str
        The full text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML-formatted blog post.
    """
    # Escape any characters that could form malicious scripts
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Insert the escaped values into the template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post