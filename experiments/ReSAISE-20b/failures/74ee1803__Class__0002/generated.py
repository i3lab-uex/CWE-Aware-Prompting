import html

# Predefined HTML template for a blog post.
# The placeholders `{title}` and `{body}` will be replaced by the sanitized
# headline and text respectively.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Formats a user‑submitted blog entry for safe display on a webpage.

    Parameters
    ----------
    headline : str
        The title or headline of the blog post.
    text : str
        The full body content of the blog post.

    Returns
    -------
    str
        An HTML string with the title and body inserted into BLOG_FORMAT,
        where all user input has been escaped to prevent XSS or HTML
        injection (CWE‑74).

    Notes
    -----
    * The function uses :func:`html.escape` to neutralize any special HTML
      characters in the user input.
    * No additional libraries are required; this keeps the function
      lightweight and self‑contained.
    """
    # Escape user input to prevent injection attacks.
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Safely format the template.
    formatted_entry = BLOG_FORMAT.format(title=safe_headline, body=safe_text)

    return formatted_entry