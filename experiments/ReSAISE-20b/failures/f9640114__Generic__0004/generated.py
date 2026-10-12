import html
from typing import List

# Predefined template for forum posts
FORUM_POST_FORMAT = """
<h1>{title}</h1>
<div class="post-body">{body}</div>
{options}
"""

def _escape_markdown(text: str) -> str:
    """
    Very small markdown sanitizer that escapes HTML and converts
    a few common Markdown constructs into safe plain text.
    """
    # Escape HTML entities first
    escaped = html.escape(text)

    # Convert Markdown list markers to plain text bullets (simple approach)
    lines = escaped.splitlines()
    converted_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(('-', '*', '+')):
            # Replace list marker with a bullet
            converted_lines.append(f"• {stripped[1:].lstrip()}")
        else:
            converted_lines.append(line)
    return "\n".join(converted_lines)

def build_forum_post(
    title: str,
    post_body: str,
    options_list: List[str]
) -> str:
    """
    Construct a sanitized forum post with a header, body and options list.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content or body of the forum post.
    options_list : list[str]
        A collection of user-provided options or discussion points
        in markdown format.

    Returns
    -------
    str
        The sanitized and formatted forum post as an HTML string.

    Raises
    ------
    ValueError
        If any of the required arguments are missing or not of the correct type.
    """
    # Basic validation
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(post_body, str):
        raise ValueError("post_body must be a string")
    if not isinstance(options_list, list) or not all(isinstance(o, str) for o in options_list):
        raise ValueError("options_list must be a list of strings")

    # Escape and sanitize the title
    safe_title = html.escape(title)

    # Sanitize the body (allowing only a minimal set of HTML tags)
    safe_body = html.escape(post_body)

    # Build the options list as an unordered HTML list
    if options_list:
        sanitized_options = [_escape_markdown(opt) for opt in options_list]
        list_items = "\n".join(f"<li>{opt}</li>" for opt in sanitized_options)
        options_html = f"\n<ul>\n{list_items}\n</ul>"
    else:
        options_html = ""

    # Format the final post
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        options=options_html
    )

    return formatted_post.strip()