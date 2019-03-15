#!/usr/bin/env python3
import os
import sys
import yaml
import logging
from logging.config import fileConfig


def print_banner(texto):
    import pyfiglet
    print(pyfiglet.figlet_format(texto))
    return


def get_conf(file):
    import yaml
    with open(file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    globals().update(cfg)
    return


def setup_logging(default_path='conf/logging.yaml', default_level=logging.INFO):
    global logger
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Failed to load configuration file. Using default configs')


#TODO: Export path and file
def set_statistics():
    import numpy as np
    import pandas as pd
    df = pd.read_csv("data/biometria-tse-dataprev.csv")
    vars = {
        "describe": df.describe().to_html()
    }
    return vars


#TODO: Export path
def generate_html(vars):
    import jinja2
    path = os.path.dirname(os.path.abspath(__file__))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
    template = "templates/geral.j2"
    html = env.get_template(template).render(vars)
    return html


#TODO: Export path and file
def write_report(html):
    report = "resultados/relatorio_geral.html"
    with open(report, "w") as result_file:
        result_file.write(html)
    return


def main():
    vars = set_statistics()
    html = generate_html(vars)
    write_report(html)


if __name__ == "__main__":
    setup_logging()
    print_banner("Created by DtpLabs!!")
    logging.info("This is an info of the root logger")
    get_conf('conf/config.yaml')
    sys.exit(main())



