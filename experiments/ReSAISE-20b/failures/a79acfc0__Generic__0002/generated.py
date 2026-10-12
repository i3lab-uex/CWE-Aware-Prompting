import html

# Example template; in a real application this would be defined elsewhere.
BLOG_FORMAT = "<article><h1>{title}</h1><div class=\"content\">{body}</div></article>"

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user‑generated blog post safely for display in HTML.

    Parameters
    ----------
    title : str
        The title of the blog post.
    body : str
        The main content of the blog post.

    Returns
    -------
    str
        A sanitized HTML string containing the formatted title and body.
    
    Raises
    ------
    ValueError
        If either `title` or `body` is empty after stripping whitespace.
    """
    if not title.strip():
        raise ValueError("Title cannot be empty.")
    if not body.strip():
        raise ValueError("Body cannot be empty.")

    # Escape HTML special characters to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)