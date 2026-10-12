import html

# Predefined HTML structure for blog posts.
BLOG_FORMAT = """
<article class="blog-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="post-body">
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
        A sanitized and HTML‑formatted string ready for inclusion in a web page.
    """
    # Escape any special characters to prevent XSS attacks
    safe_heading = html.escape(heading, quote=True)
    safe_text = html.escape(text, quote=True)

    # Preserve paragraph breaks by converting newlines to <br>
    safe_body = safe_text.replace("\n", "<br>")

    # Render the final HTML using the predefined format
    return BLOG_FORMAT.format(title=safe_heading, body=safe_body)