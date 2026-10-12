import html
from typing import List

# Example template for a forum post.  The placeholders are:
#   {header} – the title of the post
#   {body}   – the main content
#   {options}– a list of discussion points rendered as an unordered list
FORUM_POST_FORMAT = """<div class="forum-post">
  <h2>{header}</h2>
  <p>{body}</p>
  {options}
</div>"""

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a sanitized forum post from the given title, body and topics.

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
        A string containing the sanitized and formatted forum post, including the header,
        message, and safely rendered options.

    Notes
    -----
    - All user-provided content is escaped to prevent XSS attacks.
    - Markdown in `topics` is treated as plain text; no conversion to HTML is performed
      to keep the implementation simple and safe.
    """
    # Escape all user input to avoid HTML injection
    escaped_title = html.escape(title, quote=True)
    escaped_body = html.escape(body, quote=True)

    # Build an unordered list for the topics
    if topics:
        escaped_items = [
            f"<li>{html.escape(topic, quote=True)}</li>" for topic in topics
        ]
        options_html = f"<ul>\n  " + "\n  ".join(escaped_items) + "\n</ul>"
    else:
        options_html = ""

    # Render the final post using the template
    return FORUM_POST_FORMAT.format(
        header=escaped_title,
        body=escaped_body,
        options=options_html
    )