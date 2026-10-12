import html

# Predefined HTML template for a blog post.  The placeholders `{title}` and `{body}`
# will be replaced with the sanitized title and content respectively.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Formats and sanitizes a user‑submitted blog entry for safe HTML display.

    Parameters
    ----------
    headline : str
        The title or headline of the blog post.
    text : str
        The full body content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post.

    Notes
    -----
    * The function uses :func:`html.escape` to neutralize any HTML or script
      content that might be injected by an attacker.
    * ``BLOG_FORMAT`` is a minimal template; it can be extended with
      additional attributes or CSS classes as needed.
    * This implementation guards against CWE‑707 (Improper Neutralization)
      by ensuring that all user input is escaped before being inserted into
      the template.
    """
    # Escape any potentially dangerous characters in the title and body.
    safe_title = html.escape(headline, quote=True)
    # The blog body may contain legitimate line breaks and paragraphs.
    # We escape it first, then replace newlines with <br> tags to preserve
    # formatting in the rendered HTML.
    escaped_body = html.escape(text, quote=True)
    safe_body = escaped_body.replace("\n", "<br>")

    # Insert the sanitized content into the template.
    formatted_entry = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_entry