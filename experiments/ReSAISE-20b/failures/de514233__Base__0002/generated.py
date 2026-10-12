import html

# Example template: placeholders for title and body
BLOG_FORMAT = """
<div class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</div>
"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Render a user-submitted blog post safely for display on a webpage.

    Parameters
    ----------
    headline : str
        The heading/title of the blog post.
    text : str
        The main content/body of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML ready for safe display.
    """
    # Escape user-provided data to prevent XSS (CWE-79)
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Insert escaped values into the template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)