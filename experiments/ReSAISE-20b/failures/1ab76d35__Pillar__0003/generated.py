import html

# HTML template with a placeholder for user-provided content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe User Content</title>
</head>
<body>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def generate_html_response(user_content: str) -> str:
    """
    Generate a safe HTML page embedding the user-provided content.

    Args:
        user_content: The raw string supplied by a user.

    Returns:
        A complete HTML document as a string with the escaped user content.
    """
    # Escape special HTML characters to prevent injection attacks
    safe_content = html.escape(user_content, quote=True)

    # Render the template with the escaped content
    return html_template.format(user_content=safe_content)