import html
from typing import List

# A simple template with named placeholders for header, body and options.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<div class="post-body">{body}</div>
{options}
"""

def build_forum_post(title: str, post_body: str, options_list: List[str]) -> str:
    """
    Construct a sanitized forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content or body of the forum post. It is treated as plain text and
        escaped to prevent injection.
    options_list : list[str]
        A collection of user‑provided options or discussion points in markdown
        format. Each option is escaped and wrapped in a <li> tag.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post, including a header,
        body, and an unordered list of options.

    Raises
    ------
    ValueError
        If any argument is not of the expected type.
    """
    # Basic type checks to avoid misuse
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(post_body, str):
        raise ValueError("post_body must be a string")
    if not isinstance(options_list, list):
        raise ValueError("options_list must be a list")
    for opt in options_list:
        if not isinstance(opt, str):
            raise ValueError("all items in options_list must be strings")

    # Escape user input to avoid XSS and other injection attacks
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Build the options list as <ul><li>...</li></ul>
    escaped_options = []
    for opt in options_list:
        # Escape the markdown content; we do not render Markdown to HTML
        escaped_opt = html.escape(opt, quote=True)
        escaped_options.append(f"<li>{escaped_opt}</li>")
    options_html = "<ul>\n" + "\n".join(escaped_options) + "\n</ul>" if escaped_options else ""

    # Render the final post using the predefined format
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=options_html
    )