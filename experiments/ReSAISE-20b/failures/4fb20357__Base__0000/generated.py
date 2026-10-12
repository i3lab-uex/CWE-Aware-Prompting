import html

# Predefined HTML template for a blog post.
BLOG_FORMAT = """
<div class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</div>
"""

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main headline or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string ready for inclusion in a web page.

    Notes
    -----
    * The function uses `html.escape` to neutralise any HTML or JavaScript
      that a user might attempt to inject, mitigating CWE‑79 (XSS).
    * Line breaks in the description are preserved by converting them to
      `<br>` tags, which is a common lightweight approach for simple text.
    """
    # Escape user input to prevent XSS
    safe_title = html.escape(heading, quote=True)
    safe_body_text = html.escape(description, quote=True)

    # Preserve line breaks by replacing newline characters with <br>
    safe_body = safe_body_text.replace('\n', '<br>')

    # Format the final HTML using the predefined template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)