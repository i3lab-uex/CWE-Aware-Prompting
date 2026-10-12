import html
from typing import List

# Template for rendering a forum post. Placeholders: {header}, {message}, {options}
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<p>{message}</p>
<ul>
{options}
</ul>
"""

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Render a sanitized forum post from user input.

    Args:
        header (str): The title of the post.
        message (str): Body text of the post.
        options (List[str]): A list of user‑supplied options in markdown format.

    Returns:
        str: The fully rendered and sanitized forum post.
    """
    # Sanitize the header and message to prevent XSS
    safe_header = html.escape(header, quote=True)
    safe_message = html.escape(message, quote=True)

    # Convert each option into a sanitized list item
    safe_options = []
    for opt in options:
        # Escape any HTML tags or attributes inside the option
        escaped_opt = html.escape(opt, quote=True)
        # Wrap in <li> tags
        safe_options.append(f"  <li>{escaped_opt}</li>")

    # Join the list items into a single string
    options_html = "\n".join(safe_options)

    # Render the final HTML using the template
    rendered = FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options=options_html
    )

    return rendered.strip()