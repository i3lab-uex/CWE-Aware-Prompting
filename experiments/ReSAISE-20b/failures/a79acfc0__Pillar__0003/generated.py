import html

# Template for rendering a blog post.
# It contains placeholders `{title}` and `{body}` which will be safely escaped
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a blog post for safe display on a web page.

    Parameters
    ----------
    title : str
        The title of the blog post.
    body : str
        The main content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized HTML representation of the blog post.

    Notes
    -----
    * The function uses `html.escape` to neutralize any HTML or JavaScript
      that could be injected by the user, protecting against XSS attacks.
    * The resulting string is well‑formed and can be safely inserted into
      an HTML document. This mitigates CWE-707 by ensuring the output is
      properly escaped before being rendered.

    Raises
    ------
    ValueError
        If either `title` or `body` is not a string.
    """
    if not isinstance(title, str) or not isinstance(body, str):
        raise ValueError("Both title and body must be strings")

    # Escape user input to prevent injection
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Format the final HTML snippet
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)