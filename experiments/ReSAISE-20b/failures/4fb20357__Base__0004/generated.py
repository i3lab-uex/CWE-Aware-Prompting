import html

# Predefined HTML template for a blog post.  
# {title} and {body} are placeholders that will be replaced with the
# sanitized heading and description respectively.
BLOG_FORMAT = """
<article class="blog-post">
  <header>
    <h1>{title}</h1>
  </header>
  <section class="post-body">
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
        The main headline of the blog post.
    description : str
        The full text content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string ready to be embedded in a page.

    Notes
    -----
    - The function escapes all HTML special characters to prevent XSS.
    - Line breaks in the description are converted to <br> tags for
      proper formatting when displayed.
    """
    # Escape special characters in both heading and description to neutralise XSS
    safe_heading = html.escape(heading, quote=True)
    safe_description = html.escape(description, quote=True)

    # Convert newlines to <br> for readability in the browser
    safe_description = safe_description.replace("\n", "<br>\n")

    # Populate the template with the sanitized content
    return BLOG_FORMAT.format(title=safe_heading, body=safe_description)