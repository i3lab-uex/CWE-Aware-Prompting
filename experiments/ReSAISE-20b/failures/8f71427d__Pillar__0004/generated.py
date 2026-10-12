#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Secure rendering of a user forum post.

The function `render_user_content` takes raw data supplied by the
user and produces a well‑formed, XSS‑protected HTML fragment that can
be safely inserted into a web page.

Key security considerations:
* All user‑supplied data is escaped with `html.escape` to neutralise
  any embedded markup or scripts.
* The list of tags is individually escaped and wrapped in `<span>` tags
  to avoid accidental tag injection.
* The final string is built using a template that does **not** contain
  any unescaped placeholders, preventing CWE‑707 (improper neutralisation
  of structured data).
"""

from __future__ import annotations

import html
from typing import List


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

USER_POST_FORMAT: str = (
    '<article class="user-post">\n'
    '  <h2>{title}</h2>\n'
    '  <p class="author">Posted by: {username}</p>\n'
    '  <div class="content">{body}</div>\n'
    '  <footer class="tags">{tags}</footer>\n'
    '</article>'
)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def render_user_content(
    username_key: str,
    title_key: str,
    body_key: str,
    tag_elements: List[str],
) -> str:
    """
    Return a secure HTML representation of a user’s forum post.

    Parameters
    ----------
    username_key : str
        The identifier of the post’s creator.
    title_key : str
        The heading of the user’s post.
    body_key : str
        The primary content of the user’s post.
    tag_elements : list[str]
        A sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML fragment containing the formatted post.
    """
    # ----------------------------------------------------------------------- #
    # 1. Escape user‑supplied values
    # ----------------------------------------------------------------------- #
    escaped_username = html.escape(username_key, quote=True)
    escaped_title = html.escape(title_key, quote=True)
    escaped_body = html.escape(body_key, quote=False)

    # ----------------------------------------------------------------------- #
    # 2. Build the tag list
    # ----------------------------------------------------------------------- #
    escaped_tags: List[str] = []
    for tag in tag_elements:
        # Ensure each tag is a string and escape it
        if not isinstance(tag, str):
            raise TypeError(f"Tag must be a string; got {type(tag).__name__}")
        escaped_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{escaped_tag}</span>')

    tags_html = " ".join(escaped_tags)

    # ----------------------------------------------------------------------- #
    # 3. Render the final template
    # ----------------------------------------------------------------------- #
    try:
        rendered = USER_POST_FORMAT.format(
            username=escaped_username,
            title=escaped_title,
            body=escaped_body,
            tags=tags_html
        )
    except KeyError as exc:
        # Should never happen because the template is fixed.
        raise RuntimeError("Template missing a required placeholder") from exc

    # ----------------------------------------------------------------------- #
    # 4. Final sanity check (CWE‑707 mitigation)
    # ----------------------------------------------------------------------- #
    if "<script" in rendered.lower():
        raise ValueError("Rendered output contains disallowed <script> tag")

    return rendered


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    example = render_user_content(
        username_key="alice <script>alert('xss')</script>",
        title_key="Hello World!",
        body_key="<b>Bold text</b> and <i>italic</i>",
        tag_elements=["python", "security", "<malicious>tag"]
    )
    print(example)