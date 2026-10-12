import html

# Predefined format for a forum post.
FORUM_POST_FORMAT = """
<h1>{header}</h1>
<div class="post-body">{message}</div>
{options}
"""

def build_forum_post(title: str, post_body: str, options_list: list[str]) -> str:
    """
    Construct a sanitized forum post from the provided title, body and options.

    Parameters
    ----------
    title : str
        The forum post title.
    post_body : str
        Main content of the post.
    options_list : list[str]
        List of discussion points in markdown format.

    Returns
    -------
    str
        A safe, well‑formed HTML string ready for display.

    Notes
    -----
    * All user supplied content is escaped to prevent XSS attacks.
    * Options are rendered as an unordered list (<ul>).
    """
    # Sanitize title and body
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Build options list
    if options_list:
        escaped_options = [f"<li>{html.escape(opt, quote=True)}</li>" for opt in options_list]
        options_html = "<ul>\n" + "\n".join(escaped_options) + "\n</ul>"
    else:
        options_html = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=options_html
    )