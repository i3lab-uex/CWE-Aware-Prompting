import html

# Example HTML template for a blog post.  
# The placeholders {title} and {body} will be replaced with the sanitized values.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on a webpage.

    Notes
    -----
    * The function uses `html.escape` to neutralise special HTML characters,
      preventing injection attacks (CWE‑74).
    * No additional escaping is performed beyond this, as the output will be
      inserted directly into an HTML document.
    """
    # Sanitize input to avoid injection of malicious markup
    safe_heading = html.escape(heading, quote=True)
    safe_description = html.escape(description, quote=True)

    # Construct the final HTML
    formatted_post = BLOG_FORMAT.format(title=safe_heading, body=safe_description)
    return formatted_post