import html

# Predefined template for a blog post. The placeholders must be `{title}` and `{body}`.
BLOG_FORMAT = """
<div class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</div>
"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Return a sanitized and formatted HTML representation of a blog post.

    Parameters
    ----------
    headline : str
        The heading/title of the blog post.
    text : str
        The main body content of the blog post.

    Returns
    -------
    str
        A safe, well‑formed HTML string ready for rendering.

    Raises
    ------
    TypeError
        If either argument is not a string.
    ValueError
        If the template does not contain the required placeholders.
    """
    # Validate input types
    if not isinstance(headline, str):
        raise TypeError(f"headline must be a string, got {type(headline).__name__}")
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    # Ensure the template has the required placeholders
    if "{title}" not in BLOG_FORMAT or "{body}" not in BLOG_FORMAT:
        raise ValueError("BLOG_FORMAT must contain '{title}' and '{body}' placeholders")

    # Escape user input to prevent XSS
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Build the final HTML string
    formatted_post = BLOG_FORMAT.format(title=safe_headline, body=safe_text)

    # Basic sanity check: ensure no stray placeholders remain
    if "{title}" in formatted_post or "{body}" in formatted_post:
        raise RuntimeError("Unresolved placeholders detected after formatting")

    return formatted_post