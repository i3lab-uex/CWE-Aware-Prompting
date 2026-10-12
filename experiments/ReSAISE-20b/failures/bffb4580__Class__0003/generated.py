import html

# The base HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Page</title>
</head>
<body>
    <h1>User Input</h1>
    <p>{user_content}</p>
</body>
</html>
"""

def build_html_page(client_input: str) -> str:
    """
    Construct a safe HTML page by escaping the user-provided input
    before inserting it into the template.

    Parameters:
        client_input (str): Raw content provided by the user.

    Returns:
        str: A complete HTML page with the escaped user input embedded.
    """
    # Escape special characters to prevent XSS and other injection attacks
    safe_content = html.escape(client_input, quote=True)

    # Format the template with the escaped content
    return html_template.format(user_content=safe_content)