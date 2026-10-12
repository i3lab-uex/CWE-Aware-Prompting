import html
from typing import List

# Example template – adjust as needed for the actual forum system.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<div class="post-body">
{message}
</div>
<ul class="post-options">
{options}
</ul>
"""

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a sanitized forum post string.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content of the forum post.
    topics : list[str]
        A collection of discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and HTML‑escaped forum post.
    """
    # Escape title and body to avoid XSS or broken markup
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)

    # Convert each topic into a list item. Topics are treated as plain text
    # after escaping to avoid rendering unintended HTML.
    list_items = []
    for topic in topics:
        # Strip surrounding whitespace and escape
        escaped_topic = html.escape(topic.strip(), quote=False)
        list_items.append(f"<li>{escaped_topic}</li>")

    safe_options = "\n".join(list_items)

    # Populate the template
    post_html = FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=safe_options
    )

    return post_html.strip()