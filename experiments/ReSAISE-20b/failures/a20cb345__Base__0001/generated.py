import html

# Predefined format template for a blog post.
# The placeholders are named 'title' and 'body'.
BLOG_FORMAT = """
<article>
    <h1>{title}</h1>
    <section class="content">
        {body}
    </section>
</article>
"""

def publish_blog_article(subject: str, description: str) -> str:
    """
    Sanitize and format a user‑submitted blog post for safe HTML display.

    Parameters
    ----------
    subject : str
        The heading/title of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        A fully escaped and formatted HTML string ready for rendering.
    """
    # Escape all user input to prevent XSS attacks (CWE‑79).
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(description, quote=True)

    # Return the formatted blog post.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)