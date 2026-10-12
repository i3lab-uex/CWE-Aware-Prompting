import html

# Predefined HTML template for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="content">
        {body}
    </section>
</article>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on the webpage.

    Notes
    -----
    - The function uses :func:`html.escape` to prevent XSS by escaping
      any user supplied markup.
    - It also replaces newline characters with <br> tags to preserve
      paragraph breaks in plain text submissions.
    """
    # Escape HTML special characters to avoid XSS attacks
    safe_heading = html.escape(heading, quote=True)
    safe_text = html.escape(text, quote=True)

    # Preserve line breaks in the body by converting newlines to <br>
    safe_text = safe_text.replace("\n", "<br>")

    # Format the final HTML using the predefined template
    return BLOG_FORMAT.format(title=safe_heading, body=safe_text)