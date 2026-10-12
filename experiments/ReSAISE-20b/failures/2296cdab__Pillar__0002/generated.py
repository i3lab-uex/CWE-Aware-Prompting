import html

# Predefined HTML structure for blog posts.  It uses `{title}` and `{body}`
# placeholders that will be replaced by the sanitized headline and content.
BLOG_FORMAT = """
<div class="blog-post">
  <h1>{title}</h1>
  <div class="post-content">{body}</div>
</div>
"""

def format_blog_entry(headline: str, content: str) -> str:
    """
    Prepare a user‑submitted blog entry for secure web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on the webpage.

    Raises
    ------
    TypeError
        If either `headline` or `content` is not a string.
    """
    # Validate input types
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")

    # 1. Escape all HTML special characters to prevent XSS
    safe_headline = html.escape(headline, quote=True)
    safe_content  = html.escape(content, quote=True)

    # 2. Replace placeholders in the template
    formatted = BLOG_FORMAT.format(title=safe_headline, body=safe_content)

    # 3. Return the final HTML snippet
    return formatted.strip()