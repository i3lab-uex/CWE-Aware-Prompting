import html

# Template for rendering a blog post in HTML. The placeholders `{title}` and `{body}`
# will be replaced with the sanitized values.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user-generated blog post safely for display on a web page.

    Parameters
    ----------
    title : str
        The blog post title provided by the user.
    body : str
        The main content of the blog post provided by the user.

    Returns
    -------
    str
        The HTML string containing the sanitized title and body, formatted with BLOG_FORMAT.

    Notes
    -----
    * The function uses `html.escape` to neutralize any potentially dangerous HTML or
      JavaScript code that could lead to Cross‑Site Scripting (CWE-79). This ensures
      that the output is safe for inclusion in a web page without further escaping.
    * The `escape` function also converts special characters such as `<`, `>`,
      and `&` into their corresponding HTML entities.
    """
    # Sanitize inputs to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Format the sanitized content into the template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)