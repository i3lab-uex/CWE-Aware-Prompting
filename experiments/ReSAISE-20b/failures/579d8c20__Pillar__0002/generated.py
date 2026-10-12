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
    Construct an HTML page by inserting the user-provided content into a
    predefined template, ensuring that the inserted content is properly escaped
    to prevent script injection and other HTML-based attacks.

    Parameters:
        visitor_content (str): The raw content supplied by the user.

    Returns:
        str: A complete HTML document with the escaped user content embedded.
    """
    # Escape special HTML characters to neutralize potential script injection
    safe_content = html.escape(visitor_content, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)