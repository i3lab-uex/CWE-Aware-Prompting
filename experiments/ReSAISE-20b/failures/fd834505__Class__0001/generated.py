import html

# Base HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Output</title>
</head>
<body>
    <h1>User Content:</h1>
    <div id="user-content">{user_content}</div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Render an HTML page embedding the provided user input safely.

    Args:
        user_input (str): Raw text supplied by a user. May contain
                          characters that need to be escaped.

    Returns:
        str: A complete HTML document with the user input safely
             inserted into the placeholder.
    """
    # Escape special characters to prevent injection (CWE‑74).
    safe_content = html.escape(user_input, quote=True)

    # Replace the placeholder with the escaped content.
    return html_template.replace("{user_content}", safe_content)