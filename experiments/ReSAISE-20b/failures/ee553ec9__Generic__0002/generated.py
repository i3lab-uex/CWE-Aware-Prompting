import html

# The HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Message</title>
</head>
<body>
    <div class="user-message">
        {user_content}
    </div>
</body>
</html>
"""

def build_html_output(client_message: str) -> str:
    """
    Safely embed a user-provided message into an HTML template.

    Parameters
    ----------
    client_message : str
        The raw content supplied by the user that will be inserted into the template.

    Returns
    -------
    str
        A complete HTML document with the user content escaped to prevent XSS attacks.
    """
    # Escape special HTML characters to avoid injection vulnerabilities
    escaped_content = html.escape(client_message, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=escaped_content)