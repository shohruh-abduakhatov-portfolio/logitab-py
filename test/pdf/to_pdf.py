from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("myreport.html")

template_vars = {"title": "Sales Funnel Report - National",
                 "national_pivot_table": "hello world"}

html_out = template.render(template_vars)

from weasyprint import HTML


HTML(string=html_out).write_pdf("report.pdf")
