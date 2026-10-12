#!/usr/bin/env python3
"""
Secure rendering of a user's forum post.

The function `render_user_content` escapes all user-supplied content
to protect against XSS and ensures that the resulting HTML is well‑formed.
It also sanitises tag strings and wraps each in a <span> element.

CWE‑707 Mitigation: The function guarantees that all placeholders are
replaced with properly escaped data and that the resulting string is
syntactically valid HTML. No unescaped user input reaches the output.
"""

from html import escape
from typing import List

# Predefined template.  The placeholders are named to match the function arguments.
USER_POST_FORMAT = """
<article class="forum-post">
  <header>
    <h2>{title_key}</h2>
    <p class="author">Posted by: {username_key}</p>
  </header>
  <section class="content">
    {body_key}
  </section>
  <footer class="tags">
    {tag_elements}
  </footer>
</article>
"""

def render_user_content(
    username_key: str,
    title_key: str,
    body_key: str,
    tag_elements: List[str]
) -> str:
    """
    Generate a secure HTML representation of a forum post.

    Parameters
    ----------
    username_key : str
        Identifier of the post's creator.
    title_key : str
        Heading of the user's post.
    body_key : str
        Primary content of the user's post.
    tag_elements : List[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected, well‑formed HTML string.
    """
    # Escape user-supplied strings
    escaped_username = escape(username_key, quote=True)
    escaped_title = escape(title_key, quote=True)
    escaped_body = escape(body_key)

    # Wrap each tag in a <span> and escape its content
    escaped_tags = []
    for tag in tag_elements:
        # Normalize the tag: strip whitespace, collapse internal spaces,
        # and escape special characters.
        normalized = ' '.join(tag.split())
        escaped_tag = escape(normalized, quote=True)
        span_tag = f'<span class="tag">{escaped_tag}</span>'
        escaped_tags.append(span_tag)

    # Join tags with a space for readability
    tags_html = ' '.join(escaped_tags)

    # Render the final template with all placeholders replaced
    rendered = USER_POST_FORMAT.format(
        username_key=escaped_username,
        title_key=escaped_title,
        body_key=escaped_body,
        tag_elements=tags_html
    )

    # Ensure the result is well‑formed: strip leading/trailing whitespace
    return rendered.strip()