import html
from typing import List

# Example template – in real usage this would be defined elsewhere.
FORUM_POST_FORMAT = """
<h1>{header}</h1>
<div class="post-body">
{body}
</div>
<ul class="options-list">
{options}
</ul>
"""

def build_forum_post(title: str, post_body: str, options_list: List[str]) -> str:
    """
    Construct a sanitized and well‑formed forum post.

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
        A string containing the sanitized and formatted forum post, including the header,
        message body, and safely rendered options as an HTML unordered list.

    Raises
    ------
    TypeError
        If any argument is of an incorrect type.
    ValueError
        If required arguments are empty or options_list contains non‑string items.
    """
    # Basic type checks
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(post_body, str):
        raise TypeError("post_body must be a string")
    if not isinstance(options_list, list):
        raise TypeError("options_list must be a list of strings")

    # Ensure options are all strings
    if any(not isinstance(opt, str) for opt in options_list):
        raise ValueError("All items in options_list must be strings")

    # Sanitize title and body to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=False)

    # Render options as <li> elements, escaping content
    rendered_options = "\n".join(
        f"  <li>{html.escape(opt, quote=False)}</li>" for opt in options_list
    )

    # Assemble final post using the provided format template
    formatted_post = FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body.replace("\n", "<br>"),
        options=rendered_options
    )

    return formatted_post.strip()