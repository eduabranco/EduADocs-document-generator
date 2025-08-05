from jinja2 import Template

def generate_exercise_template(subject, exercises):
    template = Template("""
    # Exercise List for {{ subject }}

    {% for exercise in exercises %}
    ## Exercise {{ loop.index }}
    {{ exercise }}
    {% endfor %}
    """)

    return template.render(subject=subject, exercises=exercises)