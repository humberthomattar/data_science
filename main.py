#!/usr/bin/env python3
import os
import jinja2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("data/biometria-tse-dataprev.csv")


template_filename = "template/geral.j2"
rendered_filename = "rendered.html"
render_vars = {
    "describe": df.describe().to_html()
}

script_path = os.path.dirname(os.path.abspath(__file__))
template_file_path = os.path.join(script_path, template_filename)
rendered_file_path = os.path.join(script_path, rendered_filename)

environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
output_text = environment.get_template(template_filename).render(render_vars)

with open(rendered_file_path, "w") as result_file:
    result_file.write(output_text)