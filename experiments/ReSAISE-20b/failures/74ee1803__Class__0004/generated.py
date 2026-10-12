import html

# Pre‑defined HTML template for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-content">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Safely format a blog entry for display in HTML.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The main body content of the blog post.

    Returns
    -------
    str
        An HTML string with the title and body inserted into BLOG_FORMAT,
        with all user supplied content properly escaped to avoid HTML
        injection (CWE‑74).

    Raises
    ------
    ValueError
        If either headline or text is not a string.
    """
    if not isinstance(headline, str):
        raise ValueError("headline must be a string")
    if not isinstance(text, str):
        raise ValueError("text must be a string")

    # Escape any special HTML characters to prevent injection.
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Insert the escaped values into the template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)