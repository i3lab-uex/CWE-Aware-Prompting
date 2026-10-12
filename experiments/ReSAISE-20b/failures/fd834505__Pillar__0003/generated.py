import html

# A minimal HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Output</title>
</head>
<body>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Return an HTML page that safely embeds the provided user input.

    The function escapes any characters that could otherwise form
    executable HTML/JavaScript, mitigating XSS and CWE-707 concerns.
    If the placeholder is missing from the template an exception
    will be raised, making the bug obvious during development.

    Parameters:
        user_input (str): Raw text provided by a user.

    Returns:
        str: A fully formed HTML document with the escaped user content.
    """
    # Escape special characters to prevent script injection
    safe_content = html.escape(user_input, quote=True)

    # Ensure the placeholder exists in the template
    if "{user_content}" not in html_template:
        raise ValueError("The HTML template does not contain a {user_content} placeholder.")

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)