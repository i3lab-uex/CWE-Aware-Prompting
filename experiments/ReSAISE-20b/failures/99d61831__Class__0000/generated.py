import html

# Example template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Output</title>
</head>
<body>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_output(input_content: str) -> str:
    """
    Injects user-supplied content into an HTML template after escaping it to prevent
    injection attacks (CWE-74).

    Parameters:
        input_content (str): The dynamic content provided by the user.

    Returns:
        str: The final HTML string with escaped user content.
    """
    # Escape special HTML characters to neutralize potential injection
    safe_content = html.escape(input_content, quote=True)

    # Render the final HTML by replacing the placeholder
    return html_template.format(user_content=safe_content)