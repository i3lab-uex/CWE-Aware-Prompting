import html

# Base HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Page</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
    </style>
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
    Construct a safe HTML response by embedding escaped user content
    into a predefined template.

    Parameters:
        visitor_content (str): Raw text input from the user.

    Returns:
        str: The full HTML page with the user's content safely escaped.
    """
    # Escape any special HTML characters to prevent injection attacks
    safe_content = html.escape(visitor_content, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)