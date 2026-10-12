import html

# Predefined HTML template for a blog post.
BLOG_FORMAT = """
<div class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</div>
"""

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on a webpage.
    """
    # Escape any special HTML characters to prevent injection attacks
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(description, quote=True)

    # Inject the escaped values into the template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)