import html

# Pre‑defined HTML template for a blog post.
# Placeholders are named "title" and "body".
BLOG_FORMAT: str = """
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
    Render a user‑submitted blog post safely for display on a webpage.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The main body text of the blog post.

    Returns
    -------
    str
        A fully rendered HTML string with user input escaped to prevent XSS.

    Notes
    -----
    * Uses :func:`html.escape` to neutralize any HTML or JavaScript
      that might be injected by the user.
    * The template must contain exactly two placeholders: ``{title}`` and
      ``{body}``.  If they are missing, a :class:`KeyError` will be raised.
    """
    # Sanitize user input
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Render the template
    try:
        rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    except KeyError as exc:
        raise ValueError(
            f"Template placeholder missing: {exc}"
        ) from exc

    return rendered