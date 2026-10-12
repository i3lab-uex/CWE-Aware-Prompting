import html

# Predefined template for blog posts.
# It contains two placeholders: {title} and {body}
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Safely format a blog entry for display.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post,
        ready for safe display in HTML.

    Raises
    ------
    ValueError
        If either heading or content is not a string.
    """
    if not isinstance(heading, str) or not isinstance(content, str):
        raise ValueError("Both heading and content must be strings.")

    # Escape HTML special characters to prevent injection attacks.
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Use the predefined template to build the final HTML.
    return BLOG_FORMAT.format(title=safe_heading, body=safe_content)