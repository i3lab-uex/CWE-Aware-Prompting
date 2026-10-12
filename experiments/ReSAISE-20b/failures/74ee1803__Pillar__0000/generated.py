import html

# Predefined HTML template for a blog post.
# The placeholders {title} and {body} will be replaced with sanitized content.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Format and sanitize a user-submitted blog entry for safe HTML display.

    Args:
        headline: The title of the blog post.
        text: The full body content of the blog post.

    Returns:
        A string containing the sanitized, well‑formed HTML representation
        of the blog post.

    Raises:
        TypeError: If either argument is not a string.
    """
    if not isinstance(headline, str):
        raise TypeError(f"headline must be a string, got {type(headline).__name__}")
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    # Escape any HTML characters to prevent XSS or markup injection.
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(text, quote=True)

    # Inject sanitized content into the template.
    formatted_html = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_html