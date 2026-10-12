import html

# Pre‑defined HTML template for a blog post.
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
    Render a blog post safely for display in HTML.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The main body text of the blog post.

    Returns
    -------
    str
        A fully escaped and formatted HTML string ready for inclusion in a page.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str) or not isinstance(content, str):
        raise TypeError("headline and content must be strings")

    # Escape all user supplied data to prevent injection attacks.
    safe_title = html.escape(headline, quote=True)
    # Preserve newlines in the content by converting them to <br> tags.
    safe_body = html.escape(content, quote=True).replace('\n', '<br>\n')

    # Populate the template with sanitized data.
    rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return rendered