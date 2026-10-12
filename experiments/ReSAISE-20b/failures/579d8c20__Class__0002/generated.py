import html

# Predefined HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_response(visitor_content: str) -> str:
    """
    Construct a safe HTML response by escaping user-provided content.

    Args:
        visitor_content: The raw string supplied by the user.

    Returns:
        A complete HTML page with the escaped content inserted.
    """
    # Escape special characters to prevent injection (CWE-74).
    safe_content = html.escape(visitor_content, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)