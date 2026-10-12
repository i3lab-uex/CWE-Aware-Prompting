import html

# Predefined format for a blog post. The placeholders are replaced by the title and body.
BLOG_FORMAT = """<article>
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Safely format a user‑submitted blog post for display in an HTML page.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The main body of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML ready for rendering.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str) or not isinstance(text, str):
        raise TypeError("headline and text must be strings")

    # Escape user input to prevent XSS (CWE‑79)
    safe_title = html.escape(headline, quote=True)
    safe_body  = html.escape(text, quote=True)

    # Format the sanitized content
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return formatted_post