import html

# Pre‑defined HTML template for a blog post.
BLOG_FORMAT = (
    "<article class=\"blog-post\">\n"
    "  <h1>{title}</h1>\n"
    "  <div class=\"post-body\">\n{body}\n  </div>\n"
    "</article>"
)

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
        A string containing a sanitized, HTML‑formatted blog post.

    Notes
    -----
    * All user input is escaped using :func:`html.escape` to neutralize
      characters that could otherwise form malicious HTML or JavaScript.
    * The resulting string is safe to embed directly in a webpage served
      to other users, mitigating CWE‑79 (XSS).
    """
    # Escape title and body separately.
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Insert into the template.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return formatted_post