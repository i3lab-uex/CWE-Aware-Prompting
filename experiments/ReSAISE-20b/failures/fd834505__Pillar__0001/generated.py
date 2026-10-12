import html

# Base HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="user-content">
        {user_content}
    </div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Construct an HTML response by safely embedding user-provided content.

    Args:
        user_input (str): Content supplied by the user to be inserted into the page.

    Returns:
        str: The final HTML string with the escaped user content.
    """
    # Escape all characters that have special meaning in HTML to prevent XSS
    safe_content = html.escape(user_input, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_content)