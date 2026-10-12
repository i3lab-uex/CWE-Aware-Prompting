import html

# Predefined HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe User Page</title>
</head>
<body>
    <h1>Hello, user!</h1>
    <p>{user_content}</p>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Construct an HTML response that safely embeds the given user input.

    Parameters
    ----------
    user_input : str
        The raw content supplied by the user.

    Returns
    -------
    str
        An HTML string with the escaped user content inserted into a
        predefined template.

    Notes
    -----
    The function uses `html.escape` to convert special characters in the
    user input into their corresponding HTML entities, preventing
    injection of malicious markup or scripts.
    """
    # Escape the user input to neutralize any HTML/JS injection attempts
    safe_content = html.escape(user_input, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)