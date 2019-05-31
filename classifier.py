import json

from google.cloud import vision
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

class ClassificationResult:
    classification = None
    paragraphs = None

    def __init__(self, classification, paragraphs):
        self.classification = classification
        self.paragraphs = paragraphs

    def toJson(self):
        return json.dumps({"classification": self.classification,
                           "paragraphs": self.paragraphs})

class Classifier:
    g_image_annotator = vision.ImageAnnotatorClient()
    g_prediction_client = automl_v1beta1.PredictionServiceClient()

    def __init__(self, project_id, model_id):
        self.project_id = project_id
        self.model_id = model_id

    def classify(self, image):
        document_image = vision.types.Image(content=image)

        image_response = self.g_image_annotator.document_text_detection(image=document_image)
        annotation = image_response.full_text_annotation
        text = annotation.text

        name = 'projects/{}/locations/us-central1/models/{}'.format(self.project_id, self.model_id)
        payload = {'text_snippet': {'content': text, 'mime_type': 'text/plain'}}

        prediction = self.g_prediction_client.predict(name, payload, {})
        
        return ClassificationResult(
            self._get_classification(prediction),
            self._get_paragraphs_with_boundaries(annotation))

    def _get_classification(self, prediction):
        classification = []

        for payload in prediction.payload:
            classification.append({"class": payload.display_name, "score": payload.classification.score})

        return classification

    def _get_paragraphs_with_boundaries(self, annotation):
        paragraphs_with_boundaries = {'paragraphs': []}

        for page in annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    paragraph_text = ''
                    paragraph_boundary = []

                    for vertex in paragraph.bounding_box.vertices:
                        paragraph_boundary.append({'x': vertex.x, 'y': vertex.y})

                    for word in paragraph.words:
                        new_word = ''
                        for symbol in word.symbols:
                            new_word = new_word + symbol.text

                            if (symbol.property.HasField('detected_break')):
                                db = symbol.property.detected_break
                                if (db == vision.enums.TextAnnotation.DetectedBreak.BreakType.LINE_BREAK):
                                    new_word = new_word + '\n'
                                else:
                                    new_word = new_word + ' '

                        paragraph_text = paragraph_text + new_word

                    paragraphs_with_boundaries['paragraphs'].append({
                        'boundingBox': paragraph_boundary,
                        'text': paragraph_text
                    })

        return paragraphs_with_boundaries
