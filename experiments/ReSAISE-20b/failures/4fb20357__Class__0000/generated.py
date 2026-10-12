import html

# Predefined HTML structure for a blog post.  The placeholders {title} and {body}
# will be replaced by the sanitized heading and description respectively.
BLOG_FORMAT = """
<article class="blog-post">
    <h1>{title}</h1>
    <div class="content">{body}</div>
</article>
"""

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string ready to be embedded in a web page.

    Notes
    -----
    - The function uses `html.escape` to neutralise any HTML special characters
      in the user input, preventing injection attacks (CWE‑74).
    - The function does not alter line breaks or formatting beyond escaping,
      allowing the caller to preserve intended paragraph breaks via `<br>` tags
      or Markdown processing if desired.
    """
    # Sanitize inputs to prevent HTML injection
    safe_heading = html.escape(heading, quote=True)
    safe_description = html.escape(description, quote=True)

    # Construct the final HTML by inserting sanitized values
    return BLOG_FORMAT.format(title=safe_heading, body=safe_description)