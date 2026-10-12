import html

# Pre‑defined HTML template for a blog post.
# The placeholders {title} and {body} will be replaced with the escaped user content.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Sanitize and format a blog post for safe HTML display.

    Args:
        post_title (str): The headline or title of the blog post.
        post_body (str): The full text content of the blog post.

    Returns:
        str: A string containing the sanitized and HTML‑formatted blog post.
    
    Raises:
        TypeError: If either argument is not a string.
    """
    if not isinstance(post_title, str) or not isinstance(post_body, str):
        raise TypeError("post_title and post_body must be strings")

    # Escape special HTML characters to prevent injection (CWE‑74).
    safe_title = html.escape(post_title, quote=True)
    # For the body we also escape but allow line breaks by converting \n to <br>.
    escaped_body = html.escape(post_body, quote=True).replace('\n', '<br>')

    # Insert the sanitized values into the template.
    return BLOG_FORMAT.format(title=safe_title, body=escaped_body)