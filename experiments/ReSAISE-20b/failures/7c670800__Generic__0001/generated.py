import html

# Example template; in real usage this would be defined elsewhere
BLOG_FORMAT = """
<div class="blog-post">
  <h2>{title}</h2>
  <div class="content">{body}</div>
</div>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Return a sanitized and formatted blog post ready for safe display.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main text body of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML snippet.
    """
    # Escape any potentially dangerous characters
    safe_title = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Safely format the template
    try:
        formatted = BLOG_FORMAT.format(title=safe_title, body=safe_content)
    except KeyError as exc:
        raise ValueError(f"Template missing placeholder: {exc}") from None

    return formatted