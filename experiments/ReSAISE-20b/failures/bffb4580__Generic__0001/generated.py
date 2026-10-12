import html

# Predefined HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe User Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="user-content">
        {user_content}
    </div>
</body>
</html>
"""

def build_html_page(client_input: str) -> str:
    """
    Construct a safe HTML page by inserting the escaped user input into
    the predefined template.

    Parameters:
        client_input (str): The raw content provided by the user.

    Returns:
        str: A complete HTML page with the user's content safely embedded.
    """
    # Escape special characters to prevent XSS or script injection
    safe_content = html.escape(client_input, quote=True)

    # Format the template with the escaped content
    return html_template.format(user_content=safe_content)