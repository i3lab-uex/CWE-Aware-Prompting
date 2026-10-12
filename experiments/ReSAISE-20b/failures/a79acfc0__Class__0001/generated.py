import html

# Template used to render a blog post. The placeholders are replaced with
# sanitized values before returning the final string.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user‑generated blog post safely for display in HTML.

    Parameters
    ----------
    title : str
        The title of the blog post.
    body : str
        The main content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized title and body inserted into
        ``BLOG_FORMAT``.

    Raises
    ------
    TypeError
        If either *title* or *body* is not a string.
    """
    if not isinstance(title, str) or not isinstance(body, str):
        raise TypeError("title and body must be strings")

    # Escape all special HTML characters to prevent injection attacks
    safe_title = html.escape(title, quote=True)
    safe_body  = html.escape(body, quote=True)

    # Insert the sanitized values into the template
    rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return rendered.strip()