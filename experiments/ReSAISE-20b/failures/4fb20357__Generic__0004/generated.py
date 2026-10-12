import html

# Predefined HTML template for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-content">{body}</div>
</article>
"""

def display_blog(heading: str, description: str) -> str:
    """
    Sanitize and format a blog post for web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML-formatted blog post,
        ready for secure presentation on a webpage.

    Raises
    ------
    ValueError
        If either `heading` or `description` is not a string.
    """
    if not isinstance(heading, str):
        raise ValueError("heading must be a string")
    if not isinstance(description, str):
        raise ValueError("description must be a string")

    # Escape any HTML special characters to prevent XSS.
    safe_heading = html.escape(heading, quote=True)
    safe_description = html.escape(description, quote=True)

    # Insert the sanitized content into the template.
    return BLOG_FORMAT.format(title=safe_heading, body=safe_description)