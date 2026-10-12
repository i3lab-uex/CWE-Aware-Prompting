import html

# Pre‑defined HTML template for a blog post.
# The placeholders `{title}` and `{body}` will be replaced with the
# escaped user supplied headline and text.
BLOG_FORMAT: str = """
<article class="blog-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="content">
        {body}
    </section>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Safely format a user‑submitted blog entry for display on a webpage.

    Parameters
    ----------
    headline : str
        The headline or title of the blog post.
    text : str
        The full body content of the blog post.

    Returns
    -------
    str
        An HTML string containing the sanitized title and body,
        inserted into the predefined BLOG_FORMAT template.

    Notes
    -----
    - Uses ``html.escape`` to neutralize any HTML or script content that
      could lead to injection attacks (CWE‑74).
    - The function does not alter the structural integrity of the
      template; it only substitutes escaped values.
    """
    # Validate types to avoid accidental injection of non‑string data
    if not isinstance(headline, str) or not isinstance(text, str):
        raise TypeError("Both headline and text must be strings")

    # Escape special HTML characters to prevent XSS or injection
    safe_title = html.escape(headline, quote=True)
    # Preserve line breaks in the body by converting them to <br> tags
    safe_body = html.escape(text, quote=True).replace("\n", "<br>")

    # Insert the sanitized values into the template
    formatted_entry = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_entry