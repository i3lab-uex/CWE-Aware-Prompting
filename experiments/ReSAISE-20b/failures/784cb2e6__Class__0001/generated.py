import html
from typing import List

# Define the forum post format. The placeholders are:
#   {header} – a <h1> element containing the title
#   {body}   – a <div> with the main content
#   {options}– an unordered list (<ul>) of discussion topics
FORUM_POST_FORMAT: str = (
    "<h1>{header}</h1>\n"
    "<div class=\"post-body\">{body}</div>\n"
    "<h2>Discussion Topics</h2>\n"
    "{options}"
)

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a sanitized forum post from user-provided title, body and topics.

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
        A string containing the sanitized and formatted forum post.
    """
    # Escape all user input to prevent HTML injection (CWE-74).
    escaped_title = html.escape(title, quote=True)
    escaped_body = html.escape(body, quote=True)

    # Render each topic as a list item.  Each topic is escaped to avoid
    # injection via markdown or other markup.
    list_items = [
        f"<li>{html.escape(topic, quote=True)}</li>" for topic in topics
    ]
    options_html = f"<ul>\n{''.join(list_items)}\n</ul>"

    # Fill the template.
    post_html = FORUM_POST_FORMAT.format(
        header=escaped_title,
        body=escaped_body,
        options=options_html
    )
    return post_html