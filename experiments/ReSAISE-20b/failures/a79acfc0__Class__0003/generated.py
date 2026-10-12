import html

# Template for a blog post; placeholders are marked by {title} and {body}
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a blog post safely for display on a web page.

    Parameters
    ----------
    title : str
        The user‑supplied title of the blog post.
    body : str
        The main content/body of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑escaped string that can be safely inserted into the page.

    Raises
    ------
    ValueError
        If either title or body is empty after stripping whitespace.
    """
    if not title.strip():
        raise ValueError("Title cannot be empty.")
    if not body.strip():
        raise ValueError("Body cannot be empty.")

    # Escape special HTML characters to prevent injection (CWE‑74)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Render the final HTML
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)