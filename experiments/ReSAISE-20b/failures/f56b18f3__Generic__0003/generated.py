import html

# Predefined HTML structure for a blog post.
BLOG_FORMAT = """
<div class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</div>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Sanitize and format a blog post for safe HTML rendering.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML-formatted blog post,
        ready for secure presentation on a webpage.

    Raises
    ------
    TypeError
        If either `heading` or `text` is not a string.
    """
    if not isinstance(heading, str) or not isinstance(text, str):
        raise TypeError("Both heading and text must be strings.")

    # Escape special HTML characters to prevent XSS.
    safe_heading = html.escape(heading, quote=True)
    safe_text = html.escape(text, quote=True)

    # Replace newlines with <br> for paragraph breaks.
    safe_text = safe_text.replace("\n", "<br>")

    # Render the final HTML using the predefined format.
    return BLOG_FORMAT.format(title=safe_heading, body=safe_text)