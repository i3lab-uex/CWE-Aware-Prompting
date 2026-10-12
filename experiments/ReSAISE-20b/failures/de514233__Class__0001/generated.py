import html

# Predefined template for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-content">{body}</div>
</article>
"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Return a sanitized and formatted blog post ready for safe display.

    Parameters
    ----------
    headline : str
        The heading of the blog post.
    text : str
        The main body text of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML of the post.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str) or not isinstance(text, str):
        raise TypeError("headline and text must be strings")

    # Escape HTML special characters to prevent injection attacks.
    safe_title = html.escape(headline, quote=True)
    safe_body  = html.escape(text, quote=True)

    # Format the sanitized content using the predefined template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)