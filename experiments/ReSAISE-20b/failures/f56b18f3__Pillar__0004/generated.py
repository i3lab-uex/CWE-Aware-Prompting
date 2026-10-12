import html

# Predefined HTML structure for a blog post.
# Placeholders: {title} and {body}
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="post-body">{body}</div>
</article>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a user‑submitted blog post for secure web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post.

    Notes
    -----
    * All user input is escaped using `html.escape` to neutralize HTML
      injection attempts (CWE‑78, CWE‑79).
    * The function does not allow arbitrary tags; only the static
      `BLOG_FORMAT` template is used, preventing CWE‑707 (improper
      neutralization of structured data).
    """
    # Escape user input to avoid XSS and ensure well‑formed HTML.
    safe_heading = html.escape(heading, quote=True)
    safe_text = html.escape(text, quote=True)

    # Construct the final HTML snippet.
    formatted_post = BLOG_FORMAT.format(title=safe_heading, body=safe_text)

    return formatted_post