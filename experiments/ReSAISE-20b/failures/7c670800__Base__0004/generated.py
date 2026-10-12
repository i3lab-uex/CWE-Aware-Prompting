import html

# Predefined template for a blog post. The placeholders `{title}` and `{body}`
# will be replaced by the sanitized heading and content respectively.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def display_blog_entry(heading: str, content: str) -> str:
    """
    Return a safe, formatted HTML string for displaying a blog entry.

    Parameters
    ----------
    heading : str
        The title of the blog post.
    content : str
        The main text body of the blog post.

    Returns
    -------
    str
        An HTML string with the title and body properly escaped to prevent XSS.
    """
    # Escape user input to neutralize any HTML/JS that could lead to XSS.
    safe_title = html.escape(heading, quote=True)
    safe_body = html.escape(content, quote=True)

    # Use the predefined template to format the blog post.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)