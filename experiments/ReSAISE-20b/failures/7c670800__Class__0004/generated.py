import html

# Predefined string template for blog posts.
# It should contain placeholders `{title}` and `{body}` for the heading and content respectively.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="post-content">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Sanitize and format a user‑submitted blog post for safe display.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main body text of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted blog post,
        ready to be inserted into a webpage.

    Raises
    ------
    ValueError
        If either `heading` or `content` is not a string.
    """
    if not isinstance(heading, str) or not isinstance(content, str):
        raise ValueError("Both heading and content must be strings.")

    # Escape special HTML characters to prevent XSS or injection attacks.
    safe_title = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Format the sanitized values into the predefined template.
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_content)

    return formatted_post