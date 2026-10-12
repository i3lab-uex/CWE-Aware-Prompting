#!/usr/bin/env python3
"""
A utility to build a sanitized HTML forum entry from user supplied data.
The function escapes all user content and renders bullet points as a <ul> list.
"""

from html import escape
from typing import List

# Example template – in practice this could be loaded from a config or file.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  <ul>{bullet_points}</ul>
</div>
"""

def build_forum_entry(post_title: str, post_body: str,
                      bullet_points: List[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Args:
        post_title: The title or main topic of the forum post.
        post_body: The main body or content of the forum post.
        bullet_points: A list of discussion points in markdown format.

    Returns:
        str: A fully formatted and sanitized HTML string.
    """
    # Escape all user-provided content to prevent XSS or malformed HTML
    safe_title = escape(post_title, quote=True)
    safe_body = escape(post_body, quote=True)

    # Convert markdown bullet points into <li> elements,
    # escaping any user content within them.
    safe_bullets = []
    for point in bullet_points:
        # Basic markdown to HTML conversion: strip leading '*' or '-' and whitespace
        stripped = point.lstrip(' *-').strip()
        safe_point = escape(stripped, quote=True)
        safe_bullets.append(f"<li>{safe_point}</li>")

    bullet_html = "\n".join(safe_bullets)

    # Format the final HTML string
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        bullet_points=bullet_html
    )

# Example usage:
if __name__ == "__main__":
    title = "Best Practices for Secure Coding"
    body = ("When writing code, always consider security implications.\n"
            "For example, avoid using eval on user input.")
    points = [
        "* Use prepared statements for database queries.",
        "* Validate all inputs on the server side.",
        "* Escape output to prevent XSS attacks."
    ]
    print(build_forum_entry(title, body, points))