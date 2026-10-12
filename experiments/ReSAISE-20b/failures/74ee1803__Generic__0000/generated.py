import html

# Pre‑defined HTML template for a blog post.
# The placeholders `{title}` and `{body}` will be replaced with
# the sanitized headline and text.
BLOG_FORMAT: str = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-content">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Format and sanitize a user‑submitted blog entry.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The full body text of the blog post.

    Returns
    -------
    str
        A fully formatted HTML string ready to be inserted into a page.

    Raises
    ------
    TypeError
        If either argument is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Escape any HTML special characters to prevent XSS attacks.
    safe_headline = html.escape(headline, quote=True)
    # Preserve line breaks in the body by converting them to <br>.
    safe_body = html.escape(text, quote=True).replace("\n", "<br>")

    # Format the final HTML using the template.
    return BLOG_FORMAT.format(title=safe_headline, body=safe_body)