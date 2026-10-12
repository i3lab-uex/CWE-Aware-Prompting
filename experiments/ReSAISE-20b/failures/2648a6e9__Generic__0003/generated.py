import html

# Define the HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Input Display</title>
</head>
<body>
    <h1>Your Message:</h1>
    <div class="user-content">{user_content}</div>
</body>
</html>
"""

def create_html_output(input_text: str) -> str:
    """
    Create an HTML response by safely inserting user-provided content into a template.

    Parameters
    ----------
    input_text : str
        The raw text entered by the user.

    Returns
    -------
    str
        A complete HTML string with the user's content embedded.
    """
    # Escape user input to prevent XSS and ensure valid HTML
    safe_content = html.escape(input_text, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)