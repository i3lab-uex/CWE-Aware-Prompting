import html

# Predefined template for a blog post (simple example)
BLOG_FORMAT = """
<article>
  <h1>{heading}</h1>
  <div class="content">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Sanitize and format a user‑submitted blog entry for safe display.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main text body of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post ready for rendering in HTML.
    """
    # Escape user input to prevent XSS (CWE‑79)
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Format using the predefined template
    formatted_post = BLOG_FORMAT.format(heading=safe_heading, body=safe_content)
    return formatted_post