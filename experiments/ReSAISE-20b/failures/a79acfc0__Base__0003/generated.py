import html

# Template for rendering a blog post. Placeholders: {title} and {body}
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a blog post safely for inclusion in an HTML page.

    Parameters
    ----------
    title : str
        The user‑supplied title of the post.
    body : str
        The user‑supplied main content of the post.

    Returns
    -------
    str
        An HTML string with the title and body properly escaped to prevent XSS.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(title, str) or not isinstance(body, str):
        raise TypeError("Both title and body must be strings")

    # Escape all user input to neutralize any HTML/JS that might have been injected.
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)