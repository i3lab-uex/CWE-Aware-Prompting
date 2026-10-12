import html

# The HTML template that contains a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Submission</title>
</head>
<body>
    <h1>Your Content:</h1>
    <div>{user_content}</div>
</body>
</html>
"""

def create_html_output(input_text: str) -> str:
    """
    Create an HTML page by inserting the provided user content into a
    predefined template. The function escapes the user input to prevent
    injection attacks and ensure that the resulting page remains well‑formed.

    Args:
        input_text: The raw text supplied by a user.

    Returns:
        A string containing the complete HTML page with the escaped content.
    """
    # Escape special HTML characters to avoid breaking the markup
    safe_content = html.escape(input_text, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)