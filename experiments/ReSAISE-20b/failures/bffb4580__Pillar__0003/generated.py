import html

# Example template – in real use this would come from a config or file
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

def build_html_page(client_input: str) -> str:
    """
    Construct an HTML page by safely embedding user-provided content into a
    predefined template.

    Parameters:
        client_input (str): The raw string supplied by the user that will be
                            inserted into the HTML response.

    Returns:
        str: The complete HTML page with the user content safely escaped.
    """
    # Escape all characters that have special meaning in HTML to prevent
    # injection attacks (e.g., <, >, &, ", ').
    safe_content = html.escape(client_input, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)