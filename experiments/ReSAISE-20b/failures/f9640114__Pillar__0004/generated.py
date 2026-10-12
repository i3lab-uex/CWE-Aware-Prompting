import html
from typing import List

# A simple forum post template with placeholders for header, message and options.
FORUM_POST_FORMAT = """<h1>{header}</h1>
<div>{message}</div>
{options}
"""

def build_forum_post(title: str, post_body: str, options_list: List[str]) -> str:
    """
    Construct a sanitized forum post from the given title, body and options.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content of the forum post.
    options_list : list[str]
        A collection of discussion points or options in markdown format.

    Returns
    -------
    str
        A fully rendered HTML forum post with the header, body and options list.

    Notes
    -----
    * All user supplied content is escaped with :func:`html.escape` to avoid
      injection of malicious HTML or JavaScript.
    * The options are rendered as a well‑formed unordered list. Empty strings
      or ``None`` values in the options list are ignored.
    """
    # Sanitize title and body
    safe_title = html.escape(title or "")
    safe_body = html.escape(post_body or "")

    # Build the options list
    li_items: List[str] = []
    for opt in options_list or []:
        if not isinstance(opt, str):
            continue  # skip non‑string entries
        opt = opt.strip()
        if not opt:
            continue  # skip empty options
        li_items.append(f"<li>{html.escape(opt)}</li>")

    if li_items:
        options_html = "<ul>\n" + "\n".join(li_items) + "\n</ul>"
    else:
        options_html = ""  # no options provided

    # Assemble the final post
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=options_html
    )