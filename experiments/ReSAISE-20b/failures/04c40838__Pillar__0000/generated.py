import html
from typing import List

# Template for a forum post; placeholders will be replaced with sanitized content.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<div class="post-body">{message}</div>
{options_html}
"""

def _sanitize_markdown_links(text: str) -> str:
    """
    Convert markdown links to plain text while escaping HTML.
    Example: "[link](https://example.com)" -> "link (https://example.com)"
    """
    import re
    # Escape any existing HTML first
    escaped = html.escape(text)
    # Replace markdown links with plain text
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', escaped)

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Generate a sanitized forum post with the given header, message, and options.

    Args:
        header: The title of the post.
        message: The body text of the post.
        options: A list of user-submitted discussion options (markdown).

    Returns:
        A string containing the sanitized forum post HTML.
    """
    # Sanitize header and message to prevent XSS
    safe_header = html.escape(header)
    safe_message = _sanitize_markdown_links(message)

    # Build options HTML if any
    if options:
        option_items = []
        for opt in options:
            # Each option is sanitized and converted from markdown link to plain text
            safe_opt = _sanitize_markdown_links(opt)
            option_items.append(f"<li>{safe_opt}</li>")
        options_html = f"<ul>\n{''.join(option_items)}\n</ul>"
    else:
        options_html = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_html=options_html
    )