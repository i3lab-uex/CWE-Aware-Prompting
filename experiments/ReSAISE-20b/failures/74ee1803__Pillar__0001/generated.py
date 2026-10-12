import html

# Pre‑defined HTML template for a blog post.
# The placeholders `{headline}` and `{text}` will be replaced with the
# sanitized user input.
BLOG_FORMAT = """
<article class="blog-post">
    <header>
        <h1>{headline}</h1>
    </header>
    <section class="content">
        {text}
    </section>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Formats and sanitizes a user‑submitted blog entry for safe display on
    a web page.

    Parameters:
        headline (str): The title of the blog post.
        text (str):   The full content of the blog post.

    Returns:
        str: A fully formatted HTML string ready to be inserted into a
             web page. The headline and text are escaped to prevent
             XSS attacks.

    Raises:
        ValueError: If the provided template does not contain both
                    `{headline}` and `{text}` placeholders.
    """
    # Verify that the template contains the required placeholders
    if "{headline}" not in BLOG_FORMAT or "{text}" not in BLOG_FORMAT:
        raise ValueError("BLOG_FORMAT must contain '{headline}' and '{text}' placeholders")

    # Escape user input to neutralize HTML injection attempts
    safe_headline = html.escape(headline, quote=True)
    # For the body we allow line breaks and preserve basic formatting,
    # but still escape any malicious markup.
    safe_text = html.escape(text, quote=True).replace("\n", "<br>")

    # Use safe formatting to insert the escaped values
    return BLOG_FORMAT.format(headline=safe_headline, text=safe_text)