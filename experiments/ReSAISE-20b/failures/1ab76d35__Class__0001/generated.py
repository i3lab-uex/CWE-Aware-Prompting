import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <div id="content">{user_content}</div>
</body>
</html>
"""

def generate_html_response(user_content: str) -> str:
    """
    Generates an HTML page by safely embedding user-provided content into a template.

    Args:
        user_content (str): The raw user input to be displayed in the page.

    Returns:
        str: A complete HTML document with the user content safely escaped.
    """
    # Escape special characters to prevent XSS and injection attacks
    safe_content = html.escape(user_content, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)