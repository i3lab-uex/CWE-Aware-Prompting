#!/usr/bin/env python3
"""
Module: forum_post_creator

Provides a single public function `create_forum_post` that safely
generates an HTML forum post from user supplied content.  The function
ensures that all text is escaped to prevent XSS attacks and uses a
strict template so that the resulting output is well‑formed HTML.

The implementation follows the guidance for CWE‑707 by
ensuring that all data incorporated into the structured output is
neutralized before being rendered or transmitted.
"""

from __future__ import annotations

import html
from typing import Iterable, List

# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------

# A minimal HTML template for the forum post.
# The placeholders are replaced in order: header, body, options list.
FORUM_POST_FORMAT: str = (
    "<div class='forum-post'>\n"
    "  <h2>{header}</h2>\n"
    "  <div class='post-body'>\n{body}\n  </div>\n"
    "  <ul class='post-topics'>\n{options}\n  </ul>\n"
    "</div>"
)

# --------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------

def create_forum_post(
    title: str,
    body: str,
    topics: Iterable[str]
) -> str:
    """
    Construct a sanitized and formatted forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content or body of the forum post.  It is treated as raw
        text and escaped before being inserted into HTML.
    topics : Iterable[str]
        A collection of user‑provided discussion points or options in
        markdown format.  Each item is escaped and wrapped as an <li>
        element.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post,
        including a header, body, and an unordered list of topics.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """

    # --------------------------------------------------------------------
    # Type validation
    # --------------------------------------------------------------------
    if not isinstance(title, str):
        raise TypeError(f"title must be a str, got {type(title).__name__}")
    if not isinstance(body, str):
        raise TypeError(f"body must be a str, got {type(body).__name__}")
    if not isinstance(topics, Iterable):
        raise TypeError(f"topics must be an iterable of str, got {type(topics).__name__}")

    # --------------------------------------------------------------------
    # Escape user input to prevent XSS
    # --------------------------------------------------------------------
    escaped_title = html.escape(title, quote=True)
    escaped_body_lines: List[str] = []

    # Split body into lines to preserve line breaks in HTML
    for line in body.splitlines():
        escaped_body_lines.append(f"    {html.escape(line, quote=True)}")

    escaped_body = "\n".join(escaped_body_lines)

    # Build the <ul> list items
    escaped_options: List[str] = []
    for topic in topics:
        if not isinstance(topic, str):
            raise TypeError(f"Each topic must be a str, got {type(topic).__name__}")
        escaped_topic = html.escape(topic, quote=True)
        escaped_options.append(f"    <li>{escaped_topic}</li>")

    options_html = "\n".join(escaped_options)

    # --------------------------------------------------------------------
    # Format the final HTML
    # --------------------------------------------------------------------
    post_html = FORUM_POST_FORMAT.format(
        header=escaped_title,
        body=escaped_body,
        options=options_html
    )

    return post_html


# --------------------------------------------------------------------
# Example usage (commented out to keep module importable)
# --------------------------------------------------------------------

# if __name__ == "__main__":
#     sample_title = "Discussion: Upcoming Feature"
#     sample_body = (
#         "Hi everyone,\n"
#         "We're planning to add a new feature. Please share your thoughts.\n"
#         "Thanks!"
#     )
#     sample_topics = [
#         "Feature A",
#         "Feature B <script>alert('xss')</script>",
#         "Feature C & D"
#     ]
#
#     print(create_forum_post(sample_title, sample_body, sample_topics))