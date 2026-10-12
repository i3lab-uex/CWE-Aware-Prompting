import html
from typing import List

# Template for the forum post; placeholders will be filled with escaped content.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{header}</h2>
  <div class="post-message">{message}</div>
  {options_html}
</div>
"""

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Render a user-generated forum post.

    Parameters
    ----------
    header : str
        Title of the forum thread.
    message : str
        Body text of the post. May contain user input that must be escaped.
    options : list[str]
        List of markdown-formatted strings representing discussion options.

    Returns
    -------
    str
        A sanitized HTML fragment containing the header, message,
        and options rendered as an unordered list.

    Notes
    -----
    - All user-provided text is escaped using `html.escape` to prevent XSS.
    - The options are rendered as a `<ul>`; each option becomes an `<li>`.
      Markdown is *not* parsed – if you need markdown rendering, integrate a
      library such as `markdown2` and sanitize the output accordingly.
    """
    # Escape header and message
    safe_header = html.escape(header)
    safe_message = html.escape(message)

    # Render options as <ul> list
    if options:
        escaped_opts = [f"<li>{html.escape(opt)}</li>" for opt in options]
        options_html = f"<ul>\n{''.join(escaped_opts)}\n</ul>"
    else:
        options_html = ""

    # Format the final HTML
    post_html = FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_html=options_html
    )
    return post_html.strip()