import html

# Predefined HTML template for a blog post.
# It contains two placeholders: {title} and {body}.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Format a user‑submitted blog entry for safe display in HTML.

    Parameters
    ----------
    headline : str
        The title or headline of the blog post.
    text : str
        The full body content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized, HTML‑escaped blog post ready to be injected into a page.

    Notes
    -----
    - Uses html.escape to neutralize any HTML special characters in user input, preventing
      cross‑site scripting (CWE‑79).
    - The function does **not** perform any further sanitization (e.g., stripping scripts or
      CSS) beyond escaping; callers should ensure that only trusted content is passed if more
      stringent filtering is required.
    """
    # Escape user input to avoid injection of malicious HTML/JS
    safe_title = html.escape(headline, quote=True)
    safe_body  = html.escape(text, quote=True)

    # Insert escaped content into the template
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)