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

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

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
    # Escape any HTML special characters to prevent XSS attacks.
    safe_heading = html.escape(heading, quote=True)
    # Preserve line breaks in the body by converting them to <br> tags.
    safe_body = html.escape(description, quote=True).replace('\n', '<br>')

    # Insert the sanitized content into the predefined template.
    return BLOG_FORMAT.format(title=safe_heading, body=safe_body)