import html

# Example template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <div class="user-content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_output(input_text: str) -> str:
    """
    Generate an HTML string by inserting the escaped user-provided content
    into a predefined template.

    Args:
        input_text (str): Text supplied by the user that should appear in
                          the resulting HTML.

    Returns:
        str: The complete HTML document with user content safely embedded.
    """
    # Escape special characters to prevent injection (CWE-74).
    safe_content = html.escape(input_text, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)