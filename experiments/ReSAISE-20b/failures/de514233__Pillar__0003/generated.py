import html

# Predefined blog post format with placeholders for title and body.
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

def show_blog_post(headline: str, text: str) -> str:
    """
    Render a user‑submitted blog post safely.

    Parameters
    ----------
    headline : str
        The heading of the blog post.
    text : str
        The main body content.

    Returns
    -------
    str
        A fully sanitized HTML string ready for rendering on a web page.
    """
    # Sanitize inputs to prevent XSS and ensure well‑formed output
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # The body may contain line breaks; convert them to <br> for readability
    safe_body = safe_body.replace("\n", "<br>\n")

    # Format the final HTML using the predefined template
    rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return rendered