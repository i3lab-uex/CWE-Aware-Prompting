import html

# Predefined HTML template for a blog post.
# Use `{title}` and `{body}` as placeholders for the sanitized headline and text.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Format and sanitize a blog entry for safe display in HTML.

    Parameters
    ----------
    headline : str
        The title or headline of the blog post.
    text : str
        The full content/body of the blog post.

    Returns
    -------
    str
        A string containing the sanitized, HTML‑formatted blog post.

    Notes
    -----
    - Uses ``html.escape`` to neutralize any potentially malicious HTML or JavaScript.
    - The resulting string can be safely inserted into a web page without
      risking Cross‑Site Scripting (CWE-79).
    """
    # Sanitize inputs
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Insert sanitized content into the template
    formatted_post = BLOG_FORMAT.format(title=safe_headline, body=safe_text)

    return formatted_post