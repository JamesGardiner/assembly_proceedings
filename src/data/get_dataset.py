# -*- coding: utf-8 -*-
import os
import logging

from time import strftime


def main():
    """ Runs a script that scrapes the National Assembly for Wales website for
    the plenary speech records
    """
    logger = logging.getLogger(__name__)
    logger.info('Retrieving National Assembly for Wales data')

    # This files current path
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Root out path
    out_path = os.path.dirname(os.path.dirname(dir_path)) + '/data/raw'

    # Formatted string of current time
    dtime = strftime("%Y%m%d")

    # Out file path, name and timestamp
    out_file_path = out_path + '/ASSEMBLY_PROCEEDINGS_{}.json'.format(dtime)

    # CD to the scrapy project directory
    os.chdir(dir_path + '/get_records/')

    os.system('scrapy crawl records -o {}'.format(out_file_path))

if __name__ == '__main__':
    main()
