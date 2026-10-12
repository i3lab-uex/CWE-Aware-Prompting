import html

# Pre‑defined HTML template for blog posts.
# It should contain two placeholders: {title} and {body}.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-content">{body}</div>
</article>
"""

def render_article_page(headline: str, content: str) -> str:
    """
    Safely format a user‑submitted blog post for display in HTML.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    content : str
        The main body text of the blog post.

    Returns
    -------
    str
        An HTML string with the title and body safely escaped to prevent XSS.
    """
    # Escape user input to neutralize any HTML or script tags.
    safe_headline = html.escape(headline, quote=True)
    # For the body we also escape but keep line breaks as <br> for readability.
    safe_body = html.escape(content, quote=True).replace("\n", "<br>")

    # Insert the escaped values into the template.
    return BLOG_FORMAT.format(title=safe_headline, body=safe_body)