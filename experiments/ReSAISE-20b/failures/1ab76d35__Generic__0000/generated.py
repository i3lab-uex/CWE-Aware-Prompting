import html

# The HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Custom Response</title>
    <style>
        body {font-family: Arial, sans-serif; margin: 2rem;}
    </style>
</head>
<body>
    <h1>Your Content</h1>
    <div>{user_content}</div>
</body>
</html>
"""

def generate_html_response(user_content: str) -> str:
    """
    Generates an HTML page by embedding the provided user content into a predefined template.

    Args:
        user_content (str): The user-provided text to include in the HTML response.

    Returns:
        str: A complete HTML document with the escaped user content inserted.
    """
    # Escape special characters to prevent XSS attacks
    safe_content = html.escape(user_content, quote=True)
    # Format the template with the escaped content
    return html_template.format(user_content=safe_content)