import html

# Example template for displaying a blog post.  The placeholders `{title}` and `{body}`
# will be replaced by the sanitized values.
BLOG_FORMAT = """
<div class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</div>
"""

def render_blog_post(title: str, body: str) -> str:
    """
    Return a safe HTML representation of a user‑generated blog post.

    Parameters
    ----------
    title : str
        The raw title supplied by the user.
    body : str
        The raw body content supplied by the user.

    Returns
    -------
    str
        A string containing the sanitized title and body inserted into ``BLOG_FORMAT``.

    Notes
    -----
    * The function uses :func:`html.escape` to neutralise any HTML or JavaScript
      that might be injected by a malicious user.  This protects against
      CWE‑74 (Improper Neutralisation of Special Elements in Output Used by a Downstream Component).
    * No additional HTML tags are added to the user content, so the output remains
      safe for direct inclusion in a web page.
    """
    # Sanitize user input to prevent injection attacks
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Format the sanitized content into the template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)