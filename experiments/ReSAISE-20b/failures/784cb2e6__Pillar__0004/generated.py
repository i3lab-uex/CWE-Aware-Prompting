# create_forum_post.py

import html
from typing import List
import markdown  # pip install markdown
import bleach   # pip install bleach

# Define the forum post template. It expects placeholders:
# {header}  -> The title/header of the post
# {message} -> The main body/content of the post
# {options} -> A list of discussion points rendered as <ul>...</ul>
FORUM_POST_FORMAT = """\
<div class="forum-post">
  {header}
  <div class="post-body">{message}</div>
  <div class="post-options">{options}</div>
</div>"""

# Allowed HTML tags and attributes for safe rendering
ALLOWED_TAGS = [
    "p", "b", "i", "strong", "em",
    "ul", "ol", "li", "a", "code", "pre"
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel"]
}
ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


def _render_markdown_safe(md_text: str) -> str:
    """
    Render Markdown to HTML and then sanitize it.
    """
    # Convert Markdown to HTML
    raw_html = markdown.markdown(md_text, extensions=["extra", "sane_lists"])

    # Sanitize the resulting HTML
    clean_html = bleach.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )
    return clean_html


def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a sanitized forum post from the provided title, body,
    and list of topics (markdown strings).

    Args:
        title: The post title/subject.
        body:   The main content of the post.
        topics: A list of markdown strings representing discussion points.

    Returns:
        A string containing the fully formatted and sanitized forum post.
    """
    # Escape title to prevent HTML injection
    escaped_title = html.escape(title)

    # Render body as plain text (no markdown rendering needed)
    escaped_body = html.escape(body)

    # Render each topic as a list item
    rendered_items = []
    for topic_md in topics:
        # Convert markdown to safe HTML and wrap in <li>
        item_html = _render_markdown_safe(topic_md)
        rendered_items.append(f"<li>{item_html}</li>")

    # Combine items into an unordered list
    options_html = f"<ul>{''.join(rendered_items)}</ul>"

    # Assemble the final post
    formatted_post = FORUM_POST_FORMAT.format(
        header=f"<h1>{escaped_title}</h1>",
        message=escaped_body,
        options=options_html
    )

    return formatted_post