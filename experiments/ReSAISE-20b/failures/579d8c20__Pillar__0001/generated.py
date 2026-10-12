import html

# Base HTML template with a placeholder for user-provided content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="user-content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_response(visitor_content: str) -> str:
    """
    Construct an HTML response by inserting the escaped visitor content
    into a predefined template.

    Parameters:
        visitor_content (str): The user-supplied string to embed in the page.

    Returns:
        str: A complete HTML document with the visitor content safely escaped.
    """
    # Escape any special characters to prevent XSS or script injection.
    safe_content = html.escape(visitor_content, quote=True)

    # Render the template with the escaped content.
    return html_template.format(user_content=safe_content)