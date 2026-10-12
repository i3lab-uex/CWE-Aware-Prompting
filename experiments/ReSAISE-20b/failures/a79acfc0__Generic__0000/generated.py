import html

# Template for displaying a blog post; placeholders are {title} and {body}
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a blog post safely for display in an HTML page.

    Parameters
    ----------
    title : str
        The blog post title.
    body : str
        The main content of the blog post.

    Returns
    -------
    str
        A fully rendered HTML snippet containing the sanitized title and body.

    Raises
    ------
    ValueError
        If either `title` or `body` is None or an empty string.
    """
    if title is None or body is None:
        raise ValueError("Title and body must not be None.")
    if not title.strip() or not body.strip():
        raise ValueError("Title and body must not be empty.")

    # Escape HTML special characters to prevent XSS attacks
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False).replace('\n', '<br>')

    return BLOG_FORMAT.format(title=safe_title, body=safe_body)