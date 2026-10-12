import html

# Predefined HTML template for a blog post.
# {title} and {body} are placeholders that will be safely escaped before insertion.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on a webpage.

    Raises
    ------
    TypeError
        If either `heading` or `text` is not a string.
    """
    if not isinstance(heading, str):
        raise TypeError("heading must be a string")
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Escape special HTML characters to prevent injection attacks (CWE-74).
    safe_title = html.escape(heading, quote=True)
    safe_body  = html.escape(text, quote=True)

    # Construct the final HTML output using the template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)