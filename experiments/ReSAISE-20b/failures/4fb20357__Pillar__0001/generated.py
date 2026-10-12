import html

# Predefined HTML template for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a blog post for web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized and HTML‑formatted string ready for safe presentation on the webpage.

    Notes
    -----
    - All user input is escaped to prevent XSS (CWE-79).
    - The function does not perform any additional filtering beyond escaping,
      which is sufficient for a plain text blog post.
    """
    # Escape user-supplied data to avoid injection of malicious HTML/JS
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(description, quote=True)

    # Replace placeholders in the template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post