import html
from typing import List

# Predefined format for a forum post. Placeholders:
#   {header}  - the title of the post
#   {body}    - the main content
#   {options} - an unordered list of discussion topics
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<p>{body}</p>
{options}
"""

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a sanitized forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content or body of the forum post.
    topics : list[str]
        A collection of user-provided options or discussion points in markdown format.

    Returns
    -------
    str
        A sanitized and formatted forum post string, ready for safe inclusion in an HTML page.
    """
    # Escape title and body to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)

    # Build the unordered list of topics
    if topics:
        safe_items = []
        for topic in topics:
            # Escape each topic; markdown formatting is not processed,
            # so any special characters are neutralized.
            escaped_topic = html.escape(topic, quote=False)
            safe_items.append(f"    <li>{escaped_topic}</li>")
        options_html = "<ul>\n" + "\n".join(safe_items) + "\n</ul>"
    else:
        options_html = ""

    # Populate the template
    post_html = FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=options_html
    )
    return post_html.strip()