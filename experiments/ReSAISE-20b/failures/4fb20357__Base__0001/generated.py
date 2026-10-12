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
    Sanitize user input and format it into a safe HTML blog post.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML-formatted blog post,
        ready for secure presentation on a webpage.
    """
    # Escape special HTML characters to prevent XSS attacks (CWE-79).
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(description, quote=True)

    # Optionally convert newlines to <br> for readability.
    safe_body = safe_body.replace("\n", "<br>\n")

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)