from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("./templates"))

def render_template(template_name: str, context: dict = {}) -> str:
    template = env.get_template(template_name)
    return template.render(context)