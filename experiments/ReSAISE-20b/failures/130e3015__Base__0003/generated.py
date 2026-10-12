import html

# Predefined HTML template for a blog post. The placeholders {title} and {body}
# will be replaced with the sanitized user input.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Sanitize and format a blog post for safe HTML display.

    Parameters
    ----------
    post_title : str
        The headline or title of the blog post.
    post_body : str
        The full text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML for the blog post.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(post_title, str):
        raise TypeError("post_title must be a string")
    if not isinstance(post_body, str):
        raise TypeError("post_body must be a string")

    # Escape any HTML special characters to prevent XSS attacks.
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Insert the escaped values into the template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)