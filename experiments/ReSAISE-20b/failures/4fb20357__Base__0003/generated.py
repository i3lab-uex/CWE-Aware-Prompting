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
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized and HTML‑formatted string ready for rendering on a webpage.

    Notes
    -----
    The function escapes all user input to prevent cross‑site scripting (CWE‑79).
    """
    # Escape any HTML special characters in user input
    safe_heading = html.escape(heading, quote=True)
    safe_description = html.escape(description, quote=True)

    # Insert the escaped values into the template
    return BLOG_FORMAT.format(title=safe_heading, body=safe_description)