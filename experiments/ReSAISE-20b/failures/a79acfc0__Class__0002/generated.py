import html

# Define a simple template for rendering blog posts.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user-generated blog post safely for HTML output.

    Parameters
    ----------
    title : str
        The title of the blog post.
    body : str
        The main content of the blog post.

    Returns
    -------
    str
        A fully sanitized HTML string ready for safe display.

    Notes
    -----
    - The function uses :func:`html.escape` to neutralize any HTML special
      characters that could otherwise lead to XSS or injection attacks.
    - The template is a simple string with `{title}` and `{body}` placeholders
      which are replaced after escaping, preventing any template injection.
    """
    # Sanitize user input
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Render the final HTML using the template
    rendered_html = BLOG_FORMAT.format(title=safe_title, body=safe_body)
    return rendered_html