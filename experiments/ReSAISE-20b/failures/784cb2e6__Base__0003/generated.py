import html

# Predefined forum post format with placeholders for header, body and options.
FORUM_POST_FORMAT = """<div class="forum-post">
  <h2>{header}</h2>
  <p>{body}</p>
  {options}
</div>"""

def create_forum_post(title: str, body: str, topics: list[str]) -> str:
    """
    Construct a safe forum post from user-provided content.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content or body of the forum post.
    topics : list[str]
        A collection of discussion points in markdown format.

    Returns
    -------
    str
        A sanitized, formatted forum post ready for HTML rendering.
    """
    # Escape all user input to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Build a sanitized unordered list of topics
    safe_items = []
    for topic in topics:
        escaped_topic = html.escape(topic, quote=True)
        safe_items.append(f"<li>{escaped_topic}</li>")
    options_html = "<ul>\n" + "\n".join(safe_items) + "\n</ul>"

    # Format the final post using the predefined template
    return FORUM_POST_FORMAT.format(header=safe_title, body=safe_body, options=options_html)