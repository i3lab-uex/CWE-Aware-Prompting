import html
from typing import List

# Example template – in a real application this would be defined elsewhere.
FORUM_POST_FORMAT = """
<h1>{header}</h1>
<p>{message}</p>
{options}
"""

def build_forum_post(title: str, post_body: str, options_list: List[str]) -> str:
    """
    Construct a sanitized forum post from the provided title, body, and options.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content or body of the forum post.
    options_list : List[str]
        A collection of user‑provided options or discussion points in markdown format.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post,
        including a header, message body, and an HTML unordered list of options.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    ValueError
        If `options_list` contains non‑string items.
    """
    # Validate input types
    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")
    if not isinstance(post_body, str):
        raise TypeError(f"post_body must be a string, got {type(post_body).__name__}")
    if not isinstance(options_list, list):
        raise TypeError(f"options_list must be a list, got {type(options_list).__name__}")

    # Ensure all options are strings
    for i, opt in enumerate(options_list):
        if not isinstance(opt, str):
            raise ValueError(f"options_list[{i}] must be a string, got {type(opt).__name__}")

    # Escape HTML to prevent injection
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Convert options to an unordered list
    if options_list:
        escaped_options = [f"<li>{html.escape(opt, quote=True)}</li>" for opt in options_list]
        options_html = "<ul>\n" + "\n".join(escaped_options) + "\n</ul>"
    else:
        options_html = ""  # No options provided

    # Format the final post
    formatted_post = FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=options_html
    )

    return formatted_post.strip()