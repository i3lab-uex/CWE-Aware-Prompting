import html

# Predefined template for a blog post. The placeholders {title} and {body}
# will be replaced by the sanitized headline and text.
BLOG_FORMAT: str = """
<article>
  <header><h1>{title}</h1></header>
  <section>{body}</section>
</article>
"""

def show_blog_post(headline: str, text: str) -> str:
    """
    Return a sanitized and formatted blog post ready for safe display.

    Parameters
    ----------
    headline : str
        The heading of the blog post.
    text : str
        The main body text of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and formatted HTML snippet.
    """
    # Ensure arguments are strings; convert if necessary
    headline = str(headline) if headline is not None else ""
    text = str(text) if text is not None else ""

    # Escape HTML special characters to prevent XSS
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Insert sanitized values into the template
    formatted_post = BLOG_FORMAT.format(title=safe_headline, body=safe_text)

    # Strip leading/trailing whitespace to keep the output tidy
    return formatted_post.strip()