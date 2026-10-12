import html

# Example HTML template for a blog post.
# The placeholders {title} and {body} will be replaced by the
# sanitized user inputs.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def render_article_page(headline: str, content: str) -> str:
    """
    Render a user‑submitted blog post safely for display on a webpage.

    Parameters
    ----------
    headline : str
        The title or headline of the blog post.
    content : str
        The full text body of the blog post.

    Returns
    -------
    str
        A sanitized HTML string containing the rendered blog post.
    """
    # Sanitize user input to prevent XSS and injection attacks.
    safe_headline = html.escape(headline, quote=True)
    # For the content we escape all HTML characters but also preserve
    # line breaks by converting them to <br> tags.  This keeps the text
    # readable while preventing malicious markup.
    safe_content = html.escape(content, quote=True).replace("\n", "<br>")

    # Insert the sanitized values into the template.
    rendered = BLOG_FORMAT.format(title=safe_headline, body=safe_content)

    return rendered