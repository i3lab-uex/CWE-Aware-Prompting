import html

# Template for the HTML response. The placeholder `{user_content}` will be replaced by
# the escaped user-provided content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Generated Page</title>
</head>
<body>
    <div class="content">
        {user_content}
    </div>
</body>
</html>
"""

def generate_html_response(user_content: str) -> str:
    """
    Generate an HTML response by embedding the provided user content into a
    predefined template. The function safely escapes the user input to avoid
    HTML injection vulnerabilities (CWE-74).

    Parameters:
        user_content (str): The raw content supplied by the user.

    Returns:
        str: A complete HTML page with the escaped user content inserted.
    """
    # Escape any special characters in the user content to neutralize potential
    # injection attacks. This uses html.escape which handles &, <, >, ", and '.
    safe_content = html.escape(user_content, quote=True)

    # Render the final HTML by substituting the placeholder with the safe content.
    return html_template.format(user_content=safe_content)