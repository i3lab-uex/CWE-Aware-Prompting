import html

# Predefined HTML template for a blog post.
BLOG_FORMAT = """
<div class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</div>
"""

def format_blog_entry(headline: str, content: str) -> str:
    """
    Sanitizes and formats a blog entry for web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML-formatted blog post,
        ready for secure presentation on the webpage.

    Notes
    -----
    - Uses `html.escape` to neutralize potentially dangerous characters,
      protecting against XSS and other injection attacks.
    - No external libraries are required beyond the standard library.
    """
    # Sanitize headline and content to prevent HTML injection
    safe_title = html.escape(headline, quote=True)
    safe_body  = html.escape(content, quote=True)

    # Insert the sanitized values into the HTML template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post