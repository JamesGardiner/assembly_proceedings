# -*- coding: utf-8 -*-
import json
import logging
import os
import pickle

from ..classes.processor import Processor
from datetime import datetime


def lda_out_file_name(model, outpath=None):
    """Returns a path and filename for saving LDA models.
    Format is:
        assembly_proceedings_abstract_ldamodel_{topics}_{passes}_{iterations}.p
    """
    if not outpath:
        outpath = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.getcwd()
                )
            ),
            'data/lda_models/'
        )

    unformatted_filename = '%Y%m%d%H_project_abstract_lda_model_{}_{}_{}.p'
    date_str = datetime.now().strftime(unformatted_filename)
    file_name = date_str.format(
        model.num_topics,
        model.passes,
        model.iterations
    )
    outpath += file_name
    return outpath


def main():
    """Takes the raw data from data/raw/ASSEMBLY_PROCEEDINGS*
    and processes it into a format ready for training an LDA
    model on. This encompasses tokenizing sentences,
    lematizing the tokens, filtering English stop words, transforming
    the documents into bag of words format, and then applying a
    term frequency-inverse document frequency weighting to the resultant
    dictionary."""

    # log to tmp dir
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO,
                        filename='/tmp/github.data_analysis.log')

    # Root project folder
    dir_path = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.realpath(__file__))))

    # Root out path
    out_path = os.path.join(dir_path, 'data/interim')

    # Data folder
    in_path = os.path.join(dir_path, 'data/raw')

    # Make the outdir if it doesn't exist
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    # List of files in the raw data folder
    data_files = [file for file in os.listdir(in_path) if
                  file.split('_')[0] == "ASSEMBLY"]

    # Get the file timestamps
    dates = [os.path.splitext(file)[0].split('_')[2] for file in data_files]
    newest_date = sorted(dates)[-1]
    in_file_name = 'ASSEMBLY_PROCEEDINGS_{}.json'.format(newest_date)
    in_file = os.path.join(in_path, in_file_name)
    out_file_name = 'processor_{}.p'.format(newest_date)

    with open(in_file, 'r') as fp:
        data = json.load(fp)

    documents = []
    for plenary in data:
        for contributions in plenary['contributions']:
            documents.append(contributions.get('contribution_text'))

    processor = Processor(documents=documents)

    with open(os.path.join(out_path, out_file_name), 'wb') as fp:
        pickle.dump(processor, fp)

if __name__ == "__main__":
    main()
