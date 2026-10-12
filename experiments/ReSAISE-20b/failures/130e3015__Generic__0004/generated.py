import html

# Pre‑defined HTML template for a blog post.  The placeholders {title} and
# {body} will be replaced with the sanitized values.
BLOG_FORMAT = """
<article class="blog-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="content">
        {body}
    </section>
</article>
"""

def format_post_content(post_title: str, post_body: str) -> str:
    """
    Format a user‑submitted blog post for safe display on a webpage.

    Parameters
    ----------
    post_title : str
        The headline or title of the blog post.
    post_body : str
        The full text content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post.

    Notes
    -----
    - All user input is escaped using :func:`html.escape` to prevent XSS
      attacks.  This includes the title, body and any other user supplied
      content that might be inserted into the template.
    - The function does not modify formatting such as line breaks or
      Markdown; it simply inserts the escaped content into the template.
    """
    # Escape user input to neutralize any malicious HTML/JS
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Insert the escaped content into the template
    formatted_post = BLOG_FORMAT.format(title=safe_title, body=safe_body)

    return formatted_post