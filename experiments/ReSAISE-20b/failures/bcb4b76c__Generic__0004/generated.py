# create_forum_post.py

"""
A utility to generate a sanitized HTML representation of a forum post.

The function `create_forum_post` accepts a title, body text and a list of
discussion points written in Markdown. It renders the Markdown to HTML,
escapes any unsafe characters, sanitises the output and inserts it into a
predefined template.
"""

from __future__ import annotations

import html
from typing import List

# Third‑party libraries (install via pip if missing)
try:
    from markdown2 import Markdown
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "The 'markdown2' package is required. Install it with: pip install markdown2"
    ) from exc

try:
    import bleach
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "The 'bleach' package is required. Install it with: pip install bleach"
    ) from exc

# A simple HTML template for the forum post.
FORUM_POST_FORMAT: str = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {points}
</div>
"""

# Allowed tags and attributes for bleach sanitisation.
ALLOWED_TAGS = [
    "p",
    "b",
    "i",
    "u",
    "strong",
    "em",
    "a",
    "ul",
    "ol",
    "li",
    "blockquote",
    "code",
    "pre",
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target"],
}
# Allowed protocols for links.
ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


def _markdown_to_html(md_text: str) -> str:
    """
    Convert Markdown text to HTML using markdown2.
    The output is then sanitized with bleach to ensure safety.
    """
    # Render Markdown
    rendered = Markdown(
        extras=["fenced-code-blocks", "footnotes", "tables"]
    ).convert(md_text)

    # Sanitize the rendered HTML
    sanitized = bleach.clean(
        rendered,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,  # Remove disallowed tags instead of escaping
    )
    return sanitized


def create_forum_post(
    topic: str, text_body: str, points: List[str]
) -> str:
    """
    Create a sanitized HTML forum post.

    Parameters
    ----------
    topic : str
        The title or main topic of the forum post.
    text_body : str
        The main body or content of the forum post.
    points : list[str]
        A collection of discussion points in Markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized HTML representation of the forum post.

    Raises
    ------
    ValueError
        If any argument is not of the expected type.
    """
    # Input validation
    if not isinstance(topic, str):
        raise ValueError("topic must be a string")
    if not isinstance(text_body, str):
        raise ValueError("text_body must be a string")
    if not isinstance(points, list) or not all(isinstance(p, str) for p in points):
        raise ValueError("points must be a list of strings")

    # Escape title and body to prevent injection
    escaped_title = html.escape(topic, quote=True)
    escaped_body = _markdown_to_html(text_body)

    # Render points as an unordered list
    if points:
        rendered_points = "<ul>"
        for point in points:
            # Each point is Markdown; convert to sanitized HTML
            rendered_point = _markdown_to_html(point)
            # Wrap each point in a <li>
            rendered_points += f"<li>{rendered_point}</li>"
        rendered_points += "</ul>"
    else:
        rendered_points = ""

    # Insert into the template
    post_html = FORUM_POST_FORMAT.format(
        title=escaped_title, body=escaped_body, points=rendered_points
    )

    # Final sanitisation of the entire post (just in case)
    final_html = bleach.clean(
        post_html,
        tags=ALLOWED_TAGS + ["div", "h2"],
        attributes={
            **ALLOWED_ATTRIBUTES,
            "div": [],
            "h2": [],
        },
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )

    return final_html.strip()


# Example usage (uncomment to test)
if __name__ == "__main__":
    topic = "How to improve code quality?"
    body = """
I’ve been working on a project for a while and I’m noticing that the codebase is getting messy.
Here are some ideas I'd like to discuss:

- [ ] Refactor modules
- [x] Write unit tests
- [ ] Adopt a linter

What do you think?
"""
    points = [
        "- [ ] Refactor modules",
        "- [x] Write unit tests",
        "- [ ] Adopt a linter",
    ]

    print(create_forum_post(topic, body, points))