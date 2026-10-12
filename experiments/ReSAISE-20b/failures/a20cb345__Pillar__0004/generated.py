import html

# Predefined template for displaying blog posts.
BLOG_FORMAT = """<article>
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>"""

def publish_blog_article(subject: str, description: str) -> str:
    """
    Formats a user‑submitted blog post for safe display.

    Parameters
    ----------
    subject : str
        The title of the blog post.
    description : str
        The main body text of the blog post.

    Returns
    -------
    str
        A fully sanitized and formatted HTML snippet ready for rendering.

    Raises
    ------
    ValueError
        If either `subject` or `description` is empty or None.
    """
    if not subject:
        raise ValueError("Subject (title) cannot be empty.")
    if not description:
        raise ValueError("Description (body) cannot be empty.")

    # Escape HTML special characters to prevent XSS and ensure well‑formedness.
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(description, quote=True)

    # Render the final HTML using the template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)