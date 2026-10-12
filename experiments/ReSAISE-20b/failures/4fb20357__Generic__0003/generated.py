import html

# Predefined HTML structure for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
  <header>
    <h1>{title}</h1>
  </header>
  <section class="content">
    {body}
  </section>
</article>
"""

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on a webpage.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(heading, str):
        raise TypeError("heading must be a string")
    if not isinstance(description, str):
        raise TypeError("description must be a string")

    # Escape HTML special characters to prevent XSS.
    safe_heading = html.escape(heading, quote=True)
    # Convert newlines to <br> for preserving paragraph breaks.
    safe_description = html.escape(description, quote=True).replace("\n", "<br>")

    return BLOG_FORMAT.format(title=safe_heading, body=safe_description)