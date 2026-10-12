import html

# The HTML template containing a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div class="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_output(input_text: str) -> str:
    """
    Safely embed user-provided text into an HTML template.

    Args:
        input_text: The raw content supplied by the user.

    Returns:
        A complete HTML string with the escaped user content inserted.
    """
    # Escape special characters to prevent XSS and injection attacks
    safe_content = html.escape(input_text, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)