# -*- coding: utf-8 -*-
import logging
import os
import pickle

from ..classes import Processor
from gensim import models


def main():
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
    out_path = os.path.join(dir_path, 'models/')

    # Data folder
    in_path = os.path.join(dir_path, 'data/interim')

    # Make the outdir if it doesn't exist
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    # List of files in the raw data folder
    processor_files = [file for file in os.listdir(in_path) if
                       file.split('_')[0] == "processor"]

    # Get the file timestamps
    dates = [os.path.splitext(file)[0].split('_')[1] for
             file in processor_files]

    newest_date = sorted(dates)[-1]
    processor_file_name = 'processor_{}.p'.format(newest_date)
    processor_file = os.path.join(in_path, processor_file_name)

    with open(processor_file, 'rb') as fp:
        processor = pickle.load(fp)

    num_topics = 200
    passes = 30
    iterations = 20

    print(len(processor.dictionary))

    lda_model = models.LdaModel(processor.transformed_corpus,
                                id2word=processor.dictionary,
                                num_topics=num_topics,
                                passes=passes,
                                iterations=iterations)

    print(lda_model.show_topics())

if __name__ == "__main__":
    main()
