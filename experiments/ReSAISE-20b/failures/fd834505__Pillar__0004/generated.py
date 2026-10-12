import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="content">{user_content}</div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Render a safe HTML page by inserting escaped user input into the
    predefined html_template.

    Args:
        user_input (str): The raw string supplied by the user.

    Returns:
        str: A complete HTML page with the user content safely escaped.
    """
    # Escape all characters that could be interpreted as HTML to prevent
    # script injection or malformed markup.
    safe_content = html.escape(user_input, quote=True)

    # Format the template with the sanitized content.
    return html_template.format(user_content=safe_content)