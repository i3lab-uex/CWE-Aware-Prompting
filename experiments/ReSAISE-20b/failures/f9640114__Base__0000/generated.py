import html
from typing import List

# Template for the forum post. The placeholders are `{header}`, `{body}` and `{options}`.
FORUM_POST_FORMAT: str = """
<h1>{header}</h1>
<div class="post-body">
{body}
</div>
<div class="options">
{options}
</div>
"""

def build_forum_post(title: str, post_body: str, options_list: List[str]) -> str:
    """
    Construct a safe, HTML‑formatted forum post from user input.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content or body of the forum post. May contain user‑generated text.
    options_list : list[str]
        A collection of discussion points or options. Each item may contain markdown
        syntax but should be rendered as plain text inside <li> elements.

    Returns
    -------
    str
        A sanitized HTML string containing the formatted post. All user‑controlled
        input is escaped to prevent XSS attacks (CWE‑79).

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Validate input types
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(post_body, str):
        raise TypeError("post_body must be a string")
    if not isinstance(options_list, list) or not all(isinstance(o, str) for o in options_list):
        raise TypeError("options_list must be a list of strings")

    # Escape all user‑controlled content
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=True).replace("\n", "<br>")

    # Build the options list as <ul><li> elements
    safe_options = "<ul>"
    for option in options_list:
        escaped_option = html.escape(option, quote=True)
        safe_options += f"<li>{escaped_option}</li>"
    safe_options += "</ul>"

    # Format the final HTML
    formatted_post = FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=safe_options
    )

    return formatted_post.strip()