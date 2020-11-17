from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


async def to_pdf(file, save, data):
    location = "../templates/"
    env = Environment(loader=FileSystemLoader(location))
    template = env.get_template(file)
    location += save
    html_out = template.render(data)
    HTML(string=html_out).write_pdf(location)
    return location
