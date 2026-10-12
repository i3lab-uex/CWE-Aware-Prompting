import html

# HTML template with a placeholder for user content
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div class="user-content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_output(input_text: str) -> str:
    """
    Create an HTML response by safely inserting user-provided content
    into the predefined template.

    Parameters:
        input_text (str): The raw text supplied by the user.

    Returns:
        str: An HTML string with the escaped user content embedded.
    """
    # Escape special characters to prevent XSS or injection attacks
    safe_content = html.escape(input_text, quote=True)

    # Format the template with the escaped content
    return html_template.format(user_content=safe_content)