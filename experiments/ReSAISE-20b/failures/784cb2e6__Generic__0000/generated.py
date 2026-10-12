import html
from typing import List

# Predefined format for a forum post. Adjust the placeholders as needed.
FORUM_POST_FORMAT = """
<h1>{header}</h1>
<div>{body}</div>
{options}
"""

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a sanitized forum post string.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content or body of the forum post.
    topics : list[str]
        A collection of discussion points to be rendered as an unordered list.

    Returns
    -------
    str
        A sanitized and formatted forum post string.
    """
    # Sanitize title, body, and topics to prevent XSS or injection attacks
    safe_title = html.escape(title)
    safe_body = html.escape(body).replace("\n", "<br>")

    # Build the <ul> list of topics
    if topics:
        safe_topics = ["<li>{}</li>".format(html.escape(topic)) for topic in topics]
        options_html = "<ul>\n{}\n</ul>".format("\n".join(safe_topics))
    else:
        options_html = ""

    # Format the final post using the predefined template
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=options_html
    ).strip()