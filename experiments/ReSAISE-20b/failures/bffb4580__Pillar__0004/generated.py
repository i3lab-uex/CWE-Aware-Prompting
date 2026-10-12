import html

# Base HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def build_html_page(client_input: str) -> str:
    """
    Construct a safe HTML page by embedding the user-provided content into
    the predefined template. The input is escaped to prevent XSS or script
    injection attacks.

    Parameters:
        client_input (str): The content supplied by the user.

    Returns:
        str: A complete HTML page with the escaped user content inserted.
    """
    # Escape special HTML characters to neutralize any malicious input.
    safe_content = html.escape(client_input, quote=True)

    # Format the template with the sanitized content.
    return html_template.format(user_content=safe_content)