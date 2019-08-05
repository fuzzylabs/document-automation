import io
import os
import argparse

from classifier import Classifier

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('document', help='The document to classify')
    args = parser.parse_args()

    classifier = Classifier(os.environ['GCP_PROJECT'], os.environ['GOOGLE_MODEL_ID'])

    with io.open(args.document, 'rb') as f:
        result = classifier.classify(f.read())
        print result.classification
