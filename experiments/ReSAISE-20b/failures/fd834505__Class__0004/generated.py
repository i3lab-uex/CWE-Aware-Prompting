import html

# Base HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Output</title>
</head>
<body>
    <h1>User Content</h1>
    <div>{user_content}</div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Construct a safe HTML page by escaping user input before inserting it
    into the predefined template.

    Parameters:
        user_input (str): Content provided by the user that will be added to
                          the HTML response.

    Returns:
        str: The resulting HTML page with the escaped user content.
    """
    # Escape special HTML characters to prevent injection attacks
    safe_content = html.escape(user_input, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)