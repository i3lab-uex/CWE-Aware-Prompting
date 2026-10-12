#!/usr/bin/env python3
"""
Blog post creation utility.

The `create_blog_post` function sanitises user‑supplied heading and text,
inserts them into a pre‑defined HTML skeleton, and returns the result
ready for safe rendering on a web page.

Author: ChatGPT
"""

import html

# Predefined HTML template for blog posts.
# The placeholders `{title}` and `{body}` will be replaced by
# the escaped heading and text respectively.
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


def create_blog_post(heading: str, text: str) -> str:
    """
    Sanitize and format a blog post for web display.

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
        ready for secure presentation on the webpage.

    Raises
    ------
    TypeError
        If either `heading` or `text` is not a string.
    ValueError
        If either `heading` or `text` is an empty string after stripping.
    """
    # Basic type checks
    if not isinstance(heading, str):
        raise TypeError("`heading` must be a string")
    if not isinstance(text, str):
        raise TypeError("`text` must be a string")

    # Strip leading/trailing whitespace
    heading_clean = heading.strip()
    text_clean = text.strip()

    # Ensure non‑empty content
    if not heading_clean:
        raise ValueError("`heading` cannot be empty")
    if not text_clean:
        raise ValueError("`text` cannot be empty")

    # Escape HTML special characters to prevent XSS
    heading_escaped = html.escape(heading_clean, quote=True)
    text_escaped = html.escape(text_clean, quote=True)

    # Convert newlines to <br> tags for basic formatting
    text_escaped = text_escaped.replace("\n", "<br>\n")

    # Insert into the template
    formatted_post = BLOG_FORMAT.format(title=heading_escaped, body=text_escaped)

    return formatted_post