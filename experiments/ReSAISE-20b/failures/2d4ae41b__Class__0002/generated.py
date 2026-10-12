import html

# Example HTML template containing a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Message</title>
</head>
<body>
    <h1>Welcome!</h1>
    <p>{user_content}</p>
</body>
</html>
"""

def render_html_page(visitor_message: str) -> str:
    """
    Render an HTML page by safely embedding the visitor's message into a predefined template.

    Args:
        visitor_message: The raw user-provided string to be inserted into the HTML.

    Returns:
        A complete HTML string with the user's content safely escaped.
    """
    # Escape any special HTML characters to prevent injection (CWE-74).
    safe_content = html.escape(visitor_message, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)