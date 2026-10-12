import html

# Predefined template for blog posts.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-content">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Render a user‑submitted blog entry safely for display.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main body text of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML for the blog post.

    Notes
    -----
    - The function escapes all user‑supplied text to prevent XSS attacks.
    - It uses the global ``BLOG_FORMAT`` template, which must contain
      ``{title}`` and ``{body}`` placeholders.
    """
    # Sanitize user input to avoid injection attacks
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(content, quote=True)

    # Format the sanitized strings into the template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post