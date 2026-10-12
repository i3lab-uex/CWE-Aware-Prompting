import html
from typing import List

# Example template; in real usage this would be defined elsewhere.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  {list_section}
</div>
"""

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a sanitized forum post.

    Parameters
    ----------
    headline : str
        The title of the forum post.
    content : str
        The main body text of the post.
    items : list[str]
        A list of discussion points in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized forum post.
    """
    # Basic validation
    if not isinstance(headline, str) or not isinstance(content, str):
        raise TypeError("headline and content must be strings")

    if not isinstance(items, list) or any(not isinstance(i, str) for i in items):
        raise TypeError("items must be a list of strings")

    # Escape title and body to avoid XSS
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Convert items to a safe unordered list
    if items:
        li_elements = []
        for item in items:
            # Escape each markdown string; we do not render Markdown here
            safe_item = html.escape(item, quote=True)
            li_elements.append(f"<li>{safe_item}</li>")
        list_section = f"\n<ul>\n{''.join(li_elements)}\n</ul>"
    else:
        list_section = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        list_section=list_section
    )