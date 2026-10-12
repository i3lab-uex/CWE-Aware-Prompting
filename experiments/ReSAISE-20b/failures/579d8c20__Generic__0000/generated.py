import html

# Define the HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Page</title>
</head>
<body>
    <h1>Welcome to the Visitor Page</h1>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_response(visitor_content: str) -> str:
    """
    Construct an HTML page by inserting the user-provided content into a predefined template.
    
    The function escapes any potentially dangerous characters in `visitor_content` to prevent
    script injection attacks. It then substitutes the escaped content into the template.
    
    Parameters:
        visitor_content (str): Content provided by the user that will be added to the HTML response.
    
    Returns:
        str: The resulting HTML page with the user content safely embedded.
    """
    # Escape special HTML characters to avoid XSS vulnerabilities
    safe_content = html.escape(visitor_content, quote=True)
    
    # Return the final HTML string with escaped user content
    return html_template.format(user_content=safe_content)