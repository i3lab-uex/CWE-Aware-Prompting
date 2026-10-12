import html

# Example template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Response</title>
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
    Generates an HTML page by embedding escaped user content into a template.

    Args:
        user_content (str): The raw content supplied by the user.

    Returns:
        str: A complete HTML page with the escaped user content inserted.
    """
    # Escape special HTML characters to prevent injection attacks.
    safe_content = html.escape(user_content)

    # Render the template with the escaped content.
    return html_template.format(user_content=safe_content)