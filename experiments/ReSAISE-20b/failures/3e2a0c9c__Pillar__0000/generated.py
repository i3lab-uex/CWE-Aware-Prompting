import html
from typing import List

# Predefined HTML template for forum posts.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {list_section}
</div>
"""

def build_post_html(
    topic_title: str,
    body_text: str,
    list_items: List[str]
) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body or content of the forum post.
    list_items : List[str]
        A collection of user‑provided discussion points or options in
        markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string containing the title,
        body, and discussion points.

    Notes
    -----
    * All user supplied content is escaped using `html.escape` to prevent
      injection of malicious HTML or JavaScript.
    * If ``list_items`` is empty, the unordered list section will be omitted
      entirely.
    """
    # Escape title and body to neutralise any HTML/JS content.
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Build the list section.
    if list_items:
        safe_list_items = [
            f"<li>{html.escape(item, quote=True)}</li>"
            for item in list_items
        ]
        list_section = f"<ul>{''.join(safe_list_items)}</ul>"
    else:
        list_section = ""

    # Render the final HTML using the template.
    html_output = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        list_section=list_section
    )

    return html_output.strip()