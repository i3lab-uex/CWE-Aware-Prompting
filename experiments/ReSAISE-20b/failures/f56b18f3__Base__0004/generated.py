import html

# Predefined HTML template for a blog post
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
</article>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a user-submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized and HTML-formatted blog post ready for presentation.
    """
    # Escape user input to prevent XSS
    safe_heading = html.escape(heading, quote=True)
    safe_text = html.escape(text, quote=True)

    # Render the template with escaped content
    return BLOG_FORMAT.format(title=safe_heading, body=safe_text)