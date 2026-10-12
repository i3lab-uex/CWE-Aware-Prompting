import html

# Predefined HTML template for a blog post.
# It contains placeholders `{title}` and `{body}` that will be replaced
# by the sanitized title and content respectively.
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

def render_article_page(headline: str, content: str) -> str:
    """
    Render a user‑submitted blog post into safe HTML.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The full body text of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML for display.
    """
    # Escape any characters that could be interpreted as HTML.
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Convert newlines in the body to <br> tags for proper rendering.
    safe_body = safe_body.replace("\n", "<br>\n")

    # Insert the sanitized title and body into the template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)