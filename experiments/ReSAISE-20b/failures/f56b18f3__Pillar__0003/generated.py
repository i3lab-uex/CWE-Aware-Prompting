#!/usr/bin/env python3
"""
create_blog_post module

This module provides a single function `create_blog_post` that takes a heading
and body text, sanitizes them for safe HTML rendering, and returns the final
HTML string ready to be inserted into a web page.

The function uses `html.escape` to neutralise any potentially malicious
content, protecting against XSS and other injection attacks.

The module also defines a simple `BLOG_FORMAT` constant that contains
the HTML template with placeholders `{title}` and `{body}`.
"""

import html

# Basic HTML skeleton for a blog post. The placeholders will be replaced
# by the sanitized heading and body.
BLOG_FORMAT: str = """
<article class="blog-post">
  <header>
    <h1>{title}</h1>
  </header>
  <section class="post-content">
    {body}
  </section>
</article>
"""

def create_blog_post(heading: str, text: str) -> str:
    """
    Prepare a blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    text : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for insertion into a webpage.

    Raises
    ------
    TypeError
        If either `heading` or `text` is not a string.
    ValueError
        If the supplied template does not contain both `{title}` and `{body}`
        placeholders.
    """
    # Validate types
    if not isinstance(heading, str):
        raise TypeError(f"Expected heading to be a string, got {type(heading).__name__}")
    if not isinstance(text, str):
        raise TypeError(f"Expected text to be a string, got {type(text).__name__}")

    # Ensure the template contains required placeholders
    if "{title}" not in BLOG_FORMAT or "{body}" not in BLOG_FORMAT:
        raise ValueError("BLOG_FORMAT must contain both `{title}` and `{body}` placeholders")

    # Sanitize user input to neutralise potential XSS attacks
    safe_heading = html.escape(heading, quote=True)
    # For the body we also escape but keep line breaks as <br> for readability
    safe_text = html.escape(text, quote=True).replace("\n", "<br>")

    # Format the final HTML
    return BLOG_FORMAT.format(title=safe_heading, body=safe_text)

# Example usage (commented out):
# if __name__ == "__main__":
#     print(create_blog_post("Hello <script>", "This is a test.\nNew line."))