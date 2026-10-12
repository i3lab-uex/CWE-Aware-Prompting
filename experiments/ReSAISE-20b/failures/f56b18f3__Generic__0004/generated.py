import html

# Predefined HTML structure for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
  <header>
    <h1>{title}</h1>
  </header>
  <section class="post-content">
    {body}
  </section>
</article>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a user‑submitted blog post for secure web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string ready for rendering on the page.

    Raises
    ------
    ValueError
        If either `heading` or `text` is empty or consists only of whitespace.
    """
    if not heading.strip():
        raise ValueError("Heading must contain non‑whitespace characters.")
    if not text.strip():
        raise ValueError("Text must contain non‑whitespace characters.")

    # Escape any HTML special characters to prevent XSS.
    safe_heading = html.escape(heading, quote=True)
    # Preserve line breaks by converting newlines to <br> tags.
    safe_text = html.escape(text, quote=True).replace("\n", "<br>\n")

    # Insert the sanitized content into the predefined template.
    return BLOG_FORMAT.format(title=safe_heading, body=safe_text)