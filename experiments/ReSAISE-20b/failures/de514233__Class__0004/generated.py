import html

# Predefined template for blog posts.
# The placeholders `{title}` and `{body}` will be replaced by the sanitized inputs.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
</article>
"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Render a blog post safely for display in HTML.

    Parameters
    ----------
    headline : str
        The heading of the blog post.
    text : str
        The main body content of the blog post.

    Returns
    -------
    str
        A fully escaped and formatted HTML snippet ready for safe rendering.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Escape any HTML special characters to prevent injection attacks.
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Format the sanitized content into the predefined template.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post