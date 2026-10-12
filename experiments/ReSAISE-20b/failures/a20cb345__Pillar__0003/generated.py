#!/usr/bin/env python3
"""
publish_blog_article.py

This module provides a single function, `publish_blog_article`, which formats
a user‑submitted blog post for safe display on a web page.  The function
performs basic input validation, sanitises the title and body to prevent
cross‑site scripting (XSS) attacks, and applies a predefined template.

Security notes:
* The function uses `html.escape` to neutralise any HTML or JavaScript
  content in the title and body.  This mitigates CWE‑79 (XSS) as well
  as the CWE‑707 requirement that structured messages be well‑formed.
* It explicitly rejects non‑string inputs and disallows the presence of
  null bytes, which could otherwise be used to corrupt the output or
  bypass certain sanitisation checks.
"""

from __future__ import annotations

import html
from typing import Any

# Example template.  In a real application this would likely be loaded from
# a configuration file or templating engine.
BLOG_FORMAT: str = (
    "<article>\n"
    "  <h1>{subject}</h1>\n"
    "  <div class=\"content\">\n"
    "    {description}\n"
    "  </div>\n"
    "</article>"
)


def _validate_and_sanitize(text: Any, field_name: str) -> str:
    """
    Validates that *text* is a string, contains no null bytes, and returns
    an HTML‑escaped version of the text.

    Parameters:
        text (Any): The value to validate and escape.
        field_name (str): Name of the field for error messages.

    Returns:
        str: The sanitized string ready for inclusion in HTML output.

    Raises:
        TypeError: If *text* is not a string.
        ValueError: If *text* contains null bytes.
    """
    if not isinstance(text, str):
        raise TypeError(f"{field_name} must be a string, got {type(text).__name__}")

    if "\0" in text:
        raise ValueError(f"{field_name} must not contain null bytes")

    # Escape &, <, >, " and '
    return html.escape(text, quote=True)


def publish_blog_article(subject: str, description: str) -> str:
    """
    Formats a user‑submitted blog post for safe display on a web page.

    The function sanitises the title and body to neutralise any
    potentially malicious content, then injects them into a predefined
    HTML template.

    Parameters:
        subject (str): The heading of the blog post.
        description (str): The main text content of the blog post.

    Returns:
        str: A string containing the sanitized and formatted blog post,
             ready for safe rendering in an HTML context.

    Raises:
        TypeError: If either *subject* or *description* is not a string.
        ValueError: If either contains null bytes.
    """
    sanitized_subject = _validate_and_sanitize(subject, "subject")
    sanitized_description = _validate_and_sanitize(description, "description")

    # Insert the sanitized values into the template.
    formatted_post = BLOG_FORMAT.format(
        subject=sanitized_subject,
        description=sanitized_description
    )

    return formatted_post


# Example usage (commented out for module import safety)
if __name__ == "__main__":
    try:
        title = "Hello <script>alert('XSS');</script>"
        body = "This is a *safe* post with <b>bold</b> text."
        print(publish_blog_article(title, body))
    except Exception as exc:
        print(f"Error: {exc}")