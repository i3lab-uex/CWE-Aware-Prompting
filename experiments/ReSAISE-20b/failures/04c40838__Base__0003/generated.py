import html

# Template for a forum post.  It contains placeholders {header}, {message}
# and {options} that will be replaced by the sanitized values.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<p>{message}</p>
{options}
"""

def generate_forum_post(header: str, message: str, options: list[str]) -> str:
    """
    Render a forum post from user‑provided header, message and options.

    The function sanitizes all input to prevent cross‑site scripting (CWE‑79)
    by escaping HTML special characters.  The options are rendered as an
    unordered list (<ul>) of Markdown‑formatted strings.

    Args:
        header: The title of the post.
        message: The body text of the post.
        options: A list of option strings in Markdown format.

    Returns:
        A string containing the sanitized forum post ready for inclusion
        in an HTML page.
    """
    # Escape header and message to neutralize any embedded markup
    safe_header = html.escape(header, quote=True)
    safe_message = html.escape(message, quote=True)

    # Render options as an unordered list.  Each option is escaped
    # but retains its Markdown formatting (e.g., *bold*).  If you need
    # full Markdown rendering, replace this with a proper parser.
    if options:
        list_items = []
        for opt in options:
            # Escape the option text but preserve basic Markdown.
            escaped_opt = html.escape(opt, quote=True)
            list_items.append(f"  <li>{escaped_opt}</li>")
        safe_options = "<ul>\n" + "\n".join(list_items) + "\n</ul>"
    else:
        safe_options = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options=safe_options
    )