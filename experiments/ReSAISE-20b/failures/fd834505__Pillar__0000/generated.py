import html

# Predefined HTML template containing a placeholder for user content.
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
    Construct a safe HTML response by embedding the provided user input
    into a predefined template. The function escapes any special
    characters in the user input to prevent script injection attacks.

    Args:
        user_input (str): Content supplied by the user.

    Returns:
        str: The complete HTML page with the escaped user content.
    """
    # Escape special HTML characters to neutralize potential scripts.
    safe_content = html.escape(user_input, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)