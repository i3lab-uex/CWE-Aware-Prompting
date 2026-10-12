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
    <p>{user_content}</p>
</body>
</html>
"""

def build_html_page(client_input: str) -> str:
    """
    Construct an HTML page by safely embedding the user-provided string
    into a predefined template.

    Parameters:
        client_input (str): Raw user content to be inserted into the page.

    Returns:
        str: A complete HTML document with the user content safely escaped.
    """
    # Escape all characters that could be interpreted as HTML or JavaScript
    safe_content = html.escape(client_input, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)