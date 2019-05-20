import io
import os
import argparse

from google.cloud import vision
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

class Classifier:
    g_image_annotator = vision.ImageAnnotatorClient()
    g_prediction_client = automl_v1beta1.PredictionServiceClient()

    def __init__(self, project_id, model_id):
        self.project_id = project_id
        self.model_id = model_id

    def classify(self, document):
        with io.open(document, 'rb') as f:
            document_image = vision.types.Image(content=f.read())

            image_response = self.g_image_annotator.document_text_detection(image=document_image)
            annotation = image_response.full_text_annotation
            text = annotation.text

            name = 'projects/{}/locations/us-central1/models/{}'.format(self.project_id, self.model_id)
            payload = {'text_snippet': {'content': text, 'mime_type': 'text/plain' }}
            return self.g_prediction_client.predict(name, payload, {})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('document', help='The document to classify')
    args = parser.parse_args()

    classifier = Classifier(os.environ['GOOGLE_PROJECT_ID'], os.environ['GOOGLE_MODEL_ID'])
    print classifier.classify(args.document)
