#!/usr/bin/env python3
"""
create_blog_post module

This module defines a single function, `create_blog_post`, that safely
prepares user‑submitted blog content for display in a web page.
The function escapes all HTML special characters to prevent
cross‑site scripting (XSS) and other injection attacks.
"""

from __future__ import annotations

import html
import sys
from typing import Final

# --------------------------------------------------------------------------- #
#  Configuration – The HTML skeleton for a blog post.
#  It contains two placeholders: {title} and {body}.
# --------------------------------------------------------------------------- #
BLOG_FORMAT: Final[str] = """
<article class="blog-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="content">
        {body}
    </section>
</article>
"""

# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #
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
        A fully formatted HTML string that can be inserted into a web page.

    Raises
    ------
    ValueError
        If either `heading` or `text` is not a string or is empty.
    """
    # Validate input types
    if not isinstance(heading, str):
        raise ValueError("`heading` must be a string")
    if not isinstance(text, str):
        raise ValueError("`text` must be a string")

    # Ensure non‑empty content
    if not heading.strip():
        raise ValueError("`heading` cannot be empty or whitespace only")
    if not text.strip():
        raise ValueError("`text` cannot be empty or whitespace only")

    # Escape user input to prevent XSS and other injection attacks.
    safe_heading = html.escape(heading, quote=True)
    safe_text = html.escape(text, quote=True)

    # Build the final HTML using a controlled format string.
    # No user input is used as a formatting key, so there is no risk of
    # format string injection.
    formatted_post = BLOG_FORMAT.format(title=safe_heading, body=safe_text)

    return formatted_post

# --------------------------------------------------------------------------- #
#  Example usage (for debugging only – remove or guard with `if __name__ == "__main__":`)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        example_heading = "Welcome to My Blog!"
        example_text = (
            "Hello, world! <script>alert('XSS');</script> "
            "This is a test of the emergency broadcast system."
        )
        print(create_blog_post(example_heading, example_text))
    except Exception as exc:
        sys.stderr.write(f"Error: {exc}\n")
        sys.exit(1)