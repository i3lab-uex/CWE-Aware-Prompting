import html
from typing import List

# Predefined HTML template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  {list_section}
</div>
"""

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a forum post from the given components.

    Args:
        subject: The title of the forum post.
        text: The main body of the post. Will be escaped to avoid XSS.
        highlights: A list of discussion points (markdown strings). Each
                    item will be escaped and wrapped in an <li> element.

    Returns:
        A string containing the fully formatted HTML post, safely escaped.
    """
    # Sanitize title and body
    safe_title = html.escape(subject)
    safe_body = html.escape(text)

    # Build the discussion points list
    if highlights:
        escaped_items = [
            f"<li>{html.escape(item)}</li>" for item in highlights
        ]
        list_section = f"<ul>{''.join(escaped_items)}</ul>"
    else:
        list_section = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        list_section=list_section
    )