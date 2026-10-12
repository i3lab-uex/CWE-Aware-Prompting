import html

# Pre‑defined HTML template for a blog post.
# Use named placeholders to make the code clearer.
BLOG_FORMAT = """
<article class="blog-post">
  <h1>{title}</h1>
  <div class="content">{body}</div>
</article>
"""

def display_blog_entry(headline: str, text: str) -> str:
    """
    Return a safe HTML string for displaying a blog entry.

    Parameters
    ----------
    headline : str
        The title of the blog post.
    text : str
        The full body of the blog post.

    Returns
    -------
    str
        A sanitized, HTML‑formatted string that can be safely injected into a page.

    Notes
    -----
    - All user supplied content is escaped using :func:`html.escape` to mitigate
      Cross‑Site Scripting (CWE‑79) risks.
    - The function does not perform any additional validation beyond escaping.
      If further sanitization (e.g., Markdown rendering, allowed tags) is required,
      it should be added before calling this function.
    """
    # Escape user input to neutralize any malicious code.
    safe_title = html.escape(headline, quote=True)
    safe_body  = html.escape(text, quote=True)

    # Format the blog post using the predefined template.
    return BLOG_FORMAT.format(title=safe_title, body=safe_body)