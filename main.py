#!/usr/bin/env python3
import os
import sys
import yaml
import logging
from logging.config import fileConfig

#TODO: Documentacao das funcoes
#TODO: Avaliar a necessidade do __init__


def print_banner(texto):
    try:
        import pyfiglet
        print(pyfiglet.figlet_format(texto))
    execept Exception as e:
        logger.erro('print_banner: ' + str(e))
    return


def get_conf(file):
    try:
        with open(file, 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        globals().update(cfg)
    except Exception as e:
        logger.error('get_conf: ' + str(e))
    return


#TODO externalizar default_path
def setup_logging(default_path='conf/logging.yaml', default_level=logging.INFO):
    import coloredlogs
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print(e)
                print('Erro na configuracao do Log. Usando configuracao padrao')
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Erro na configuracao do Log. Usando configuracao padrao')
    return



#TODO: Export path
def generate_html(vars, template='templates/geral.j2'):
    try:
        import jinja2
        path = os.path.dirname(os.path.abspath(__file__))
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
        html = env.get_template(template).render(vars)
        return html
    except Exception as e:
        logger.error('generate_html: ' + str(e))
        return        


#TODO: Export path and file
def write_report(html, report='saida/relatorio_geral.html'):
    try:
        with open(report, "w") as r:
            r.write(html)
        return
    except Exception as e:
        logger.error('write_report: ' + str(e))
        return


#TODO: Export path and file
def set_statistics(filename='data/biometria-tse-dataprev.csv'):
    try:
        import numpy as np
        import pandas as pd
        df = pd.read_csv(filename)
        vars = {
            "describe": df.describe().to_html()
            }
        return vars
    except Exception as e:
        logger.error('set_statistics: ' + str(e))
        return


def main():
    try:
        vars = set_statistics()
        html = generate_html(vars)
        write_report(html)
    except Exception as e:
        logger.error('main: ' + str(e))
    return


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger('app')
    get_conf('conf/config.yaml')
    logger.info(cfg['app'])
    print_banner("Dtp.Labs")
    sys.exit(main())



