import html

# HTML template with a placeholder for user content
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Content Display</title>
</head>
<body>
    <!-- User content goes here -->
    {user_content}
</body>
</html>
"""

def construct_html_response(content: str) -> str:
    """
    Injects the provided user content into an HTML template after escaping it
    to prevent XSS and related injection attacks.

    Args:
        content: The raw user-provided string to be displayed in the HTML page.

    Returns:
        A fully-formed HTML string with the escaped user content inserted.
    """
    # Escape special characters in user content
    safe_content = html.escape(content, quote=True)

    # Safely format the template with the escaped content
    return html_template.format(user_content=safe_content)