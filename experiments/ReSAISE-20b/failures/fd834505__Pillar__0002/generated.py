import html

# Base HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Construct an HTML page embedding the provided user input in a safe manner.

    Args:
        user_input (str): Content supplied by the user that will be inserted
                          into the HTML response.

    Returns:
        str: The complete HTML page with user content safely escaped.
    """
    # Escape special HTML characters to prevent script injection and
    # ensure the output is well-formed (CWE-707 mitigation).
    safe_content = html.escape(user_input, quote=True)

    # Format the template with the escaped content.
    return html_template.format(user_content=safe_content)