import html

# Predefined template for formatting a blog post.
# It contains two placeholders: {title} and {body}.
BLOG_FORMAT = """
<article class="blog-post">
  <h2>{title}</h2>
  <div class="content">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Return a safe HTML representation of a user‑submitted blog entry.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main text body of the blog post.

    Returns
    -------
    str
        A string containing sanitized and formatted HTML ready for display.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(heading, str) or not isinstance(content, str):
        raise TypeError("Both heading and content must be strings")

    # Escape any HTML special characters to prevent XSS attacks.
    safe_title = html.escape(heading, quote=True)
    safe_body  = html.escape(content, quote=True)

    # Format the final output using the predefined template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)