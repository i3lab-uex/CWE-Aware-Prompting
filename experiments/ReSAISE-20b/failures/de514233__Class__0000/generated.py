import html

# Predefined template for blog posts.
BLOG_FORMAT = """<article>
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Return a sanitized and formatted blog post ready for safe display.

    Parameters
    ----------
    headline : str
        The heading of the blog post.
    text : str
        The main text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post.
    """
    # Escape any HTML special characters to prevent injection
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Format the sanitized content into the template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post