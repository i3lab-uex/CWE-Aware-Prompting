import html
from typing import List

# Example template; in real usage this would be imported from a config module
FORUM_POST_FORMAT = """<h1>{header}</h1>
<p>{body}</p>
{options}
"""

def construct_forum_content(heading: str, content: str, choices: List[str]) -> str:
    """
    Construct a forum post with a heading, body and a list of options.
    
    Parameters
    ----------
    heading : str
        Title or subject line of the forum post.
    content : str
        Main body text of the forum post.
    choices : list[str]
        User-provided options or discussion points in markdown format.

    Returns
    -------
    str
        Sanitized and formatted forum post string.
    
    Notes
    -----
    All user-provided data is HTML‑escaped to mitigate injection attacks (CWE‑74).
    """
    # Sanitize the heading and body
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(content, quote=True)

    # Build the unordered list of options
    if choices:
        list_items = "\n".join(f"<li>{html.escape(choice, quote=True)}</li>" for choice in choices)
        safe_options = f"<ul>\n{list_items}\n</ul>"
    else:
        safe_options = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        header=safe_heading,
        body=safe_body,
        options=safe_options
    )