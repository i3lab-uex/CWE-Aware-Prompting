import html

# Template for the forum post.
# Placeholders: {header}, {message}, {options}
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<div>{message}</div>
{options}
"""

def create_forum_post(title: str, body: str, topics: list[str]) -> str:
    """
    Construct a sanitized forum post from user-provided content.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content or body of the forum post.
    topics : list[str]
        A collection of user-provided options or discussion points
        in markdown format.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post,
        including the header, message, and safely rendered options.

    Notes
    -----
    - All user input is escaped using html.escape to prevent XSS.
    - Markdown syntax in topics is treated as plain text; no markdown
      rendering is performed. If markdown conversion is desired,
      it should be done *after* escaping to avoid injection.
    """
    # Escape user-provided strings
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Build the options list as an unordered HTML list
    if topics:
        safe_items = [
            f"<li>{html.escape(topic, quote=True)}</li>" for topic in topics
        ]
        options_html = f"<ul>{''.join(safe_items)}</ul>"
    else:
        options_html = ""

    # Render the final post using the predefined format
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=options_html
    )