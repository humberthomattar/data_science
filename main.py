#!/usr/bin/env python3
import os
import sys
import yaml
import logging
from logging.config import fileConfig

#TODO: Documentacao das funcoes


def print_banner(texto):
    try:
        import pyfiglet
        logger.debug('O banner funcionara corretamente com o log level INFO.')
        print(
            pyfiglet.figlet_format(texto)
            )
    except Exception as e:
        logger.erro('print_banner: ' + str(e))
    return


def get_conf(file):
    try:
        logger.debug('Recuperando as configuracoes da rotina => ' + str(file))
        with open(file, 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        globals().update(cfg)
        logger.debug('Configuracoes recuperadas com sucesso. => ' + str(cfg))
    except Exception as e:
        logger.error('get_conf: ' + str(e))
    return


def setup_logging(loggername, path='./conf/logging.yaml', default_level='DEBUG'):
    import coloredlogs
    try:
        global logger
        with open(path, 'rt') as f:    
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            logger = logging.getLogger(loggername)
            coloredlogs.install(logger=logger, level=logger.level)
            logger.debug('Logger configurado corretamente. => log level: ' +  
                str(logger.level) + ' ' + str(path))
    except Exception as e:
        print(str(e) + 'Erro na configuracao do Log. Usando configuracao padrao')
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
    return


def generate_html(vars, template):
    logger.info('Iniciando a geracao do html.')
    logger.debug(str(template) + str(vars))
    try:
        import jinja2
        path = os.path.dirname(os.path.abspath(__file__))
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
        html = env.get_template(template).render(vars)
        logger.info('HTML gerado com sucesso.')
        return html
    except Exception as e:
        logger.error('generate_html: ' + str(e))
        return        


def write_report(html, report):
    logger.info('Iniciando a escrita do relatorio: => ' + str(report))
    try:
        with open(report, "w") as r:
            r.write(html)
        logger.info('Relatorio gravado com sucesso.')
        return
    except Exception as e:
        logger.error('write_report: ' + str(e))
        return


def set_statistics(filename):
    logger.info('Iniciando a analise do arquivo: ' + filename)
    try:
        import numpy as np
        import pandas as pd
        df = pd.read_csv(filename)
        pd.set_option('colheader_justify', 'center')
        vars = {
            "describe": df.describe().to_html(
                classes='table table-hover table-sm'
                )
            }
        logger.info('Término da análise do arquivo.')
        return vars
    except Exception as e:
        logger.error('set_statistics: ' + str(e))
        return


def main():
    try:
        logger.info('Inicio do programa')
        vars = set_statistics(input['path'] + input['filename'])
        html = generate_html(vars, './templates/geral.j2')
        write_report(html, (output['path'] + output['reportname']))
        logger.info('Programa finalizado.')
    except Exception as e:
        logger.error('main: ' + str(e))
    return 0


if __name__ == "__main__":
    setup_logging(loggername='app')
    get_conf('conf/config.yaml')
    print_banner(app['banner'])
    sys.exit(main())
