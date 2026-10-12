import html

# Example template used by the forum system.  The placeholders are
# replaced with the header, message body and an HTML unordered list.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<div class="post-body">
{message}
</div>
<ul class="options">
{options}
</ul>
"""

def construct_forum_content(heading: str, content: str, choices: list[str]) -> str:
    """
    Construct a forum post string that safely renders user-provided content.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body of the forum post.  Will be escaped to avoid injection.
    choices : list[str]
        A collection of user-provided options or discussion points.  Each
        choice is rendered as a list item in an HTML unordered list.

    Returns
    -------
    str
        The fully formatted, sanitized forum post.
    """
    # Escape all user supplied text to neutralize special HTML characters.
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the list items; each item is escaped individually.
    list_items = []
    for choice in choices:
        safe_choice = html.escape(choice, quote=True)
        list_items.append(f"<li>{safe_choice}</li>")

    safe_options = "\n".join(list_items)

    # Populate the template
    forum_post = FORUM_POST_FORMAT.format(
        header=safe_heading,
        message=safe_content,
        options=safe_options
    )

    return forum_post.strip()