import html
from typing import List

# A minimal forum post template.  The placeholders are `{header}`, `{body}` and `{options}`.
FORUM_POST_FORMAT = """
<h1>{header}</h1>
<div class="post-body">{body}</div>
<ul class="options">
{options}
</ul>
"""

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a forum post with the given title, body and topics.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content or body of the forum post.
    topics : list[str]
        A collection of user‑provided options or discussion points in markdown format.

    Returns
    -------
    str
        A sanitized and formatted forum post string that can be safely embedded in HTML.

    Raises
    ------
    ValueError
        If any of the required arguments are empty.
    """
    if not title or not body:
        raise ValueError("title and body must be non-empty strings")

    # Sanitize the title and body to avoid HTML injection.
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Render each topic as a list item.  Topics are first escaped and then
    # wrapped in <li> tags.  The function assumes the topics are simple
    # markdown fragments; complex Markdown rendering is beyond this scope.
    rendered_topics = []
    for topic in topics:
        # Escape any special HTML characters to neutralize injection.
        escaped_topic = html.escape(topic, quote=True)
        rendered_topics.append(f"  <li>{escaped_topic}</li>")

    options_html = "\n".join(rendered_topics)

    # Build the final post using the predefined format.
    forum_post = FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=options_html
    )

    return forum_post.strip()