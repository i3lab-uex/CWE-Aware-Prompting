import html

# Pre‑defined HTML template for a blog post.
# The placeholders {title} and {body} will be replaced safely.
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

def display_blog_entry(headline: str, text: str) -> str:
    """
    Safely format and return an HTML representation of a blog entry.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The main body/content of the blog post.

    Returns
    -------
    str
        A sanitized HTML string ready for rendering in a browser.

    Raises
    ------
    ValueError
        If either argument is not a string or is empty.
    """
    # Basic type and emptiness checks
    if not isinstance(headline, str) or not isinstance(text, str):
        raise ValueError("Both headline and text must be strings.")
    if not headline.strip() or not text.strip():
        raise ValueError("Headline and text cannot be empty.")

    # Escape HTML special characters to prevent injection (CWE‑74)
    safe_title = html.escape(headline, quote=True)
    # Convert newlines to <br> for preserving paragraph breaks
    safe_body = html.escape(text, quote=True).replace("\n", "<br>")

    # Use str.format to insert the escaped content into the template
    formatted_entry = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_entry