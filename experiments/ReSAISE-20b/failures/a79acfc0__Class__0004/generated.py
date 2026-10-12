import html

# Template for displaying a blog post; placeholders are replaced by sanitized values.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
</article>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Render a user‑generated blog post safely for HTML display.

    Parameters
    ----------
    title : str
        The user‑supplied title of the post.
    body : str
        The main content of the post.

    Returns
    -------
    str
        A fully sanitized HTML snippet that can be safely inserted into a page.

    Notes
    -----
    - Uses :func:`html.escape` to neutralize any characters that could be
      interpreted as HTML or JavaScript, mitigating CWE‑74.
    - No additional templating engine is required; simple string formatting
      suffices because all user input has been escaped.
    """
    # Escape special HTML characters to prevent injection attacks.
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Render the final HTML using the provided template.
    rendered = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return rendered