import html

# Predefined HTML template for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
</article>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string ready for rendering on a web page.

    Raises
    ------
    ValueError
        If either `heading` or `text` is empty after stripping whitespace.
    """
    # Basic validation
    if not heading or not heading.strip():
        raise ValueError("Heading must not be empty.")
    if not text or not text.strip():
        raise ValueError("Text must not be empty.")

    # Escape user input to prevent XSS (CWE-79)
    safe_heading = html.escape(heading, quote=True)
    safe_text = html.escape(text, quote=True)

    # Optionally preserve newlines as <br> tags
    safe_text = safe_text.replace("\n", "<br>\n")

    # Format the final HTML
    return BLOG_FORMAT.format(title=safe_heading, body=safe_text)