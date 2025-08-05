from jinja2 import Template

def generate_summary_template(content):
    template = Template("""
    # Summary Template

    ## Title: {{ title }}

    ### Summary:
    {{ summary }}

    ### Key Points:
    {% for point in key_points %}
    - {{ point }}
    {% endfor %}
    """)

    return template.render(title=content.get('title', 'Untitled'), 
                            summary=content.get('summary', 'No summary provided.'), 
                            key_points=content.get('key_points', []))