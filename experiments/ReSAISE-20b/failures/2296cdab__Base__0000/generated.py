import html

# A simple, reusable HTML skeleton for blog posts.
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
    Prepare a user‑submitted blog entry for safe web display.

    Parameters
    ----------
    headline : str
        The main heading or subject of the blog post.
    content : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        An HTML string containing the sanitized headline and body,
        ready to be inserted into a web page.

    Notes
    -----
    * The function uses `html.escape` to neutralize any HTML special
      characters, preventing cross‑site scripting (CWE‑79).
    * No additional HTML tags are allowed in the input; any markup
      is escaped.
    """
    # Sanitize user inputs by escaping HTML special characters.
    safe_headline = html.escape(headline, quote=True)
    safe_content = html.escape(content, quote=True)

    # Format the sanitized values into the predefined blog structure.
    formatted = BLOG_FORMAT.format(title=safe_headline, body=safe_content)

    return formatted.strip()