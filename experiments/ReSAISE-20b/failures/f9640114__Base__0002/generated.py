import html

# Predefined template for the forum post.
FORUM_POST_FORMAT = """
<h1>{title}</h1>
<div class="post-body">{body}</div>
{options}
"""

def build_forum_post(title: str, post_body: str, options_list: list[str]) -> str:
    """
    Construct a sanitized and formatted forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content or body of the forum post.
    options_list : list[str]
        A collection of user‑provided options or discussion points in
        markdown format.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post,
        including the header, body, and options as an HTML unordered list.

    Raises
    ------
    ValueError
        If any of the arguments are not of the expected type.
    """
    # Basic type checks
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(post_body, str):
        raise ValueError("post_body must be a string")
    if not isinstance(options_list, list) or not all(isinstance(o, str) for o in options_list):
        raise ValueError("options_list must be a list of strings")

    # Escape user input to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Build the options as an unordered list
    if options_list:
        safe_options = "<ul>\n"
        for opt in options_list:
            # Escape each option to avoid injection
            escaped_opt = html.escape(opt, quote=True)
            safe_options += f"  <li>{escaped_opt}</li>\n"
        safe_options += "</ul>"
    else:
        safe_options = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        options=safe_options
    ).strip()