import html
from typing import List

# Predefined HTML template for a forum post.
# The placeholders {title}, {body} and {list_items}
# will be replaced by the function below.
FORUM_POST_FORMAT: str = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {list_items}
</div>
"""

def build_post_html(topic_title: str, body_text: str, list_items: List[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body content of the forum post.
    list_items : List[str]
        A collection of user‑provided discussion points or options
        (in markdown format, but treated as plain text).

    Returns
    -------
    str
        A fully formatted and escaped HTML string containing the title,
        body, and an unordered list of discussion points.

    Notes
    -----
    - All user input is escaped with `html.escape` to avoid injection
      vulnerabilities (CWE‑74).
    - Markdown is not rendered; it is treated as plain text to keep the
      function simple and safe. If Markdown rendering is required,
      a dedicated library (e.g., `markdown2`) should be used in a
      controlled environment.
    """
    # Escape all user‑supplied content
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Build the <ul> with escaped list items
    if list_items:
        ul_parts = ['<ul>']
        for item in list_items:
            safe_item = html.escape(item, quote=True)
            ul_parts.append(f'  <li>{safe_item}</li>')
        ul_parts.append('</ul>')
        safe_list = '\n'.join(ul_parts)
    else:
        # If no items, omit the list section entirely
        safe_list = ''

    # Format the final HTML
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        list_items=safe_list
    ).strip()