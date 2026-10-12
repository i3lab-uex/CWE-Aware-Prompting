import html

# Define the HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dynamic Page</title>
</head>
<body>
    {user_content}
</body>
</html>
"""

def build_html_page(page_content: str) -> str:
    """
    Build a complete HTML page by inserting escaped user-provided content
    into the predefined template.

    Parameters:
        page_content (str): The raw HTML or text supplied by the user.

    Returns:
        str: A fully formed HTML document with the user content safely escaped.
    """
    # Escape special characters to prevent XSS or markup injection
    safe_content = html.escape(page_content, quote=True)

    # Format the template with the escaped content
    return html_template.format(user_content=safe_content)