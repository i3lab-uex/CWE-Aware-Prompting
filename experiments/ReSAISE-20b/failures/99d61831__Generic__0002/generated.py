import html

# Define the HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <div class="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_output(input_content: str) -> str:
    """
    Produce a complete HTML string by injecting escaped user content into
    the predefined template.

    Parameters:
        input_content (str): The dynamic content supplied by the user.

    Returns:
        str: A safe HTML string with the user's content properly escaped.
    """
    # Escape special characters to prevent XSS or markup injection.
    safe_content = html.escape(input_content, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)