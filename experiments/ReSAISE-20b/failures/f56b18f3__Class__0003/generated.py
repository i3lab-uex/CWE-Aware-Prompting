import html

# Predefined HTML template for a blog post.
# The placeholders {title} and {body} will be replaced with escaped user input.
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

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a blog post for safe HTML display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML-formatted string ready for rendering on the web page.

    Notes
    -----
    * The function escapes all special HTML characters in both the heading and the body to
      prevent injection attacks (CWE‑74). The escaping is performed with ``html.escape`` which
      converts characters such as &, <, >, ", and ' into their corresponding HTML entities.
    * The body text is also split into paragraphs by double newlines to preserve formatting
      while still escaping content. Each paragraph is wrapped in a ``<p>`` tag.
    """
    # Escape the heading and body content
    safe_heading = html.escape(heading, quote=True)

    # Preserve line breaks by converting paragraphs
    paragraphs = [html.escape(p.strip(), quote=True) for p in text.splitlines() if p.strip()]
    safe_body = "\n".join(f"<p>{para}</p>" for para in paragraphs)

    # Format the final HTML
    return BLOG_FORMAT.format(title=safe_heading, body=safe_body)