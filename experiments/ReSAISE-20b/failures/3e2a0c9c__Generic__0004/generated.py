import html

# Predefined HTML template for a forum post.
# The placeholders {title}, {body} and {list_items} will be replaced
# by the sanitized arguments passed to `build_post_html`.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {list_items}
</div>
"""

def build_post_html(topic_title: str, body_text: str, list_items: list[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main content of the forum post.
    list_items : list[str]
        A collection of discussion points or options in markdown format.

    Returns
    -------
    str
        Fully formatted and sanitized HTML string.
    """
    # Escape all user-provided content to avoid XSS or injection attacks
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Convert markdown list items into <li> tags.
    # We assume each string is a plain line; advanced markdown parsing
    # is outside the scope of this function.
    if list_items:
        safe_list = "<ul>\n"
        for item in list_items:
            escaped_item = html.escape(item, quote=True)
            safe_list += f"  <li>{escaped_item}</li>\n"
        safe_list += "</ul>"
    else:
        safe_list = ""

    # Format the final HTML using the predefined template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        list_items=safe_list
    )