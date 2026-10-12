import html

# Predefined HTML structure for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main headline or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on the webpage.

    Notes
    -----
    - All user input is escaped using ``html.escape`` to prevent
      injection attacks such as XSS.
    - The function does not perform any additional validation of length or
      content; such checks should be handled by the caller if needed.
    """
    # Escape user input to neutralize any HTML/JS injection attempts
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(description, quote=True)

    # Render the blog post using the predefined format
    rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return rendered