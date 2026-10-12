import html

# Template for a blog post. The placeholders {title} and {body}
# will be replaced with the sanitized user input.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a blog post safely for display in a web page.

    Parameters
    ----------
    title : str
        The title of the blog post. Must be a string.
    body : str
        The main content of the blog post. Must be a string.

    Returns
    -------
    str
        A fully rendered HTML snippet with the title and body safely escaped.

    Raises
    ------
    TypeError
        If either `title` or `body` is not a string.
    """
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(body, str):
        raise TypeError("body must be a string")

    # Escape user input to neutralize any malicious HTML/JS.
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Format the final HTML using the template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)