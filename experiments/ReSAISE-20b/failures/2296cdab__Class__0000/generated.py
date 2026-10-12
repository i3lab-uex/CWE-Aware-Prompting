import html

# Predefined HTML structure for a blog post.
# The placeholders `{title}` and `{body}` will be replaced by the
# escaped headline and content respectively.
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

def format_blog_entry(headline: str, content: str) -> str:
    """
    Sanitize and format a blog entry for safe web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML-formatted blog post,
        ready for secure presentation on the webpage.

    Notes
    -----
    The function escapes all HTML special characters in both the headline
    and content to prevent injection attacks (CWE‑74).  No additional
    HTML tags are allowed; if markup is desired, it must be added by the
    caller in a controlled manner.
    """
    # Escape special characters to neutralize any injected HTML/JS.
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Render the blog post using the predefined template.
    return BLOG_FORMAT.format(title=safe_headline, body=safe_content)