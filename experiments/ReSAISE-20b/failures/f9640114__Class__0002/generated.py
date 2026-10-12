import html

# Predefined format for forum posts.
FORUM_POST_FORMAT = """
<h1>{header}</h1>
<div class="post-body">{message}</div>
{options}
"""

def build_forum_post(title: str, post_body: str, options_list: list[str]) -> str:
    """
    Construct a sanitized forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content or body of the forum post.
    options_list : list[str]
        A collection of user-provided options or discussion points in markdown format.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post, including the header,
        message, and safely rendered options.

    Notes
    -----
    All user-supplied content is escaped using `html.escape` to prevent injection
    (CWE‑74). Markdown in options is preserved as plain text; no further rendering is
    performed to avoid accidental execution of unintended markup.
    """
    # Escape user input to neutralize special HTML characters.
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Build the options list as an unordered HTML list.
    if options_list:
        escaped_items = [f"<li>{html.escape(opt, quote=True)}</li>" for opt in options_list]
        options_html = "<ul>\n" + "\n".join(escaped_items) + "\n</ul>"
    else:
        options_html = ""

    # Format the final post using the predefined template.
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=options_html
    )