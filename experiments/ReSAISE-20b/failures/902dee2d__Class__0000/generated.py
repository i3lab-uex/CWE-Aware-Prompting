import html
from typing import List

# Pre‑defined template for the forum post.  The placeholders are marked
# with {title}, {body} and {list_items}.
FORUM_POST_FORMAT = """
<h2>{title}</h2>
<div class="post-body">{body}</div>
<ul>{list_items}</ul>
"""

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a sanitized forum post.

    Parameters
    ----------
    headline : str
        The title of the post.
    content : str
        The main body text of the post.
    items : list[str]
        Discussion points supplied by the user.  Each item is expected
        to be plain text; if it contains markdown or HTML, it will be
        escaped.

    Returns
    -------
    str
        A fully formatted HTML snippet that can safely be embedded in a
        page or sent to downstream components.

    Notes
    -----
    All user‑supplied content is passed through html.escape to neutralise
    any characters that could alter the markup or inject scripts.  This
    protects against CWE‑74 (Improper Neutralization of Special Elements).
    """
    # Escape the headline and content to avoid HTML injection.
    safe_title = html.escape(headline, quote=True)
    safe_body = html.escape(content, quote=True)

    # Build the list items; each is escaped and wrapped in <li>.
    safe_items = []
    for item in items:
        escaped_item = html.escape(item, quote=True)
        safe_items.append(f"<li>{escaped_item}</li>")
    list_html = "\n".join(safe_items)

    # Format the final HTML using the template.
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        list_items=list_html
    )