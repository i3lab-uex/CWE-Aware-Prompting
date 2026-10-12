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
    <h1>User Content</h1>
    <div>{user_content}</div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Construct a safe HTML page by inserting the user-provided content
    into a predefined template.

    Parameters
    ----------
    user_input : str
        The raw content supplied by the user.

    Returns
    -------
    str
        A complete HTML document with the escaped user content embedded.
    """
    # Escape any characters that could be interpreted as HTML/JS
    safe_content = html.escape(user_input, quote=True)

    # Format the template with the escaped content
    return html_template.format(user_content=safe_content)