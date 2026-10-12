import html

# Predefined HTML structure for a blog post.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def format_blog_entry(headline: str, content: str) -> str:
    """
    Prepare a blog post for secure web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized and HTML‑formatted string ready for presentation.

    Raises
    ------
    ValueError
        If the headline is empty or contains only whitespace.
    """
    if not headline or headline.strip() == "":
        raise ValueError("Headline cannot be empty")

    # Escape user-supplied text to prevent XSS and other injection attacks.
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Render the final HTML using the predefined format.
    return BLOG_FORMAT.format(title=safe_headline, body=safe_content)