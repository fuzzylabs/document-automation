import json

from google.cloud import vision
from google.cloud import language
#from google.cloud import automl_v1beta1
#from google.cloud.automl_v1beta1.proto import service_pb2

class ClassificationResult:
    width = None
    height = None
    classification = None
    paragraphs = None
    entities = None
    text = ""

    def __init__(self, width, height, classification, paragraphs, entities):
        self.width = width
        self.height = height
        self.classification = classification
        self.paragraphs = paragraphs
        self.entities = entities
        for paragraph in paragraphs['paragraphs']:
            self.text = self.text + paragraph['text'] + '\n'

    def toJson(self):
        return json.dumps({
            "width": self.width,
            "height": self.height,
            "text": self.text,
            #"classification": self.classification,
            "paragraphs": self.paragraphs,
            "entities": self.entities})

class Classifier:
    g_image_annotator = vision.ImageAnnotatorClient()
    #g_prediction_client = automl_v1beta1.PredictionServiceClient()
    g_language_client = language.LanguageServiceClient()

    def __init__(self, project_id, model_id):
        self.project_id = project_id
        self.model_id = model_id

    def classify(self, image):
        document_image = vision.types.Image(content=image)

        # OCR the image extracting the text
        image_response = self.g_image_annotator.document_text_detection(image=document_image)
        annotation = image_response.full_text_annotation
        paragraphs = self._get_paragraphs_with_boundaries(annotation)
        text = ""
        for paragraph in paragraphs['paragraphs']:
            text = text + paragraph['text'] + '\n'

        # Run the text through a classification model
        #name = 'projects/{}/locations/us-central1/models/{}'.format(self.project_id, self.model_id)
        #payload = {'text_snippet': {'content': text, 'mime_type': 'text/plain'}}
        #prediction = self.g_prediction_client.predict(name, payload, {})

        # Extract interesting entities from the text
        document = language.types.Document(content=text, type=language.enums.Document.Type.PLAIN_TEXT)
        entity_result = self.g_language_client.analyze_entities(document)
        entities = self._get_entities(entity_result)

        return ClassificationResult(
            annotation.pages[0].width,
            annotation.pages[0].height,
            None, #self._get_classification(prediction),
            paragraphs,
            entities)

    def _get_entities(self, entity_result):
        def mk_entry(e):
            return {'value': e.name, 'metadata': map(lambda x: {x[0]: x[1]}, e.metadata.items())}


        def render_type(t):
            try:
                return language.types.Entity.Type.Name(t)
            except:
                return str(t)

        entity_map = {}
        for entity in entity_result.entities:
            if entity.type in [language.types.Entity.ADDRESS, language.types.Entity.LOCATION, language.types.Entity.PHONE_NUMBER, language.types.Entity.PERSON, language.types.Entity.ORGANIZATION, language.types.Entity.DATE]:
                e_type = render_type(entity.type)
                if not e_type in entity_map:
                    entity_map[e_type] = []
                    entity_map[e_type].append(mk_entry(entity))

        return entity_map

    #def _get_classification(self, prediction):
    #    classification = []

    #    for payload in prediction.payload:
    #        classification.append({"class": payload.display_name, "score": payload.classification.score})

    #   return classification

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

                            if symbol.property.HasField('detected_break'):
                                db = symbol.property.detected_break
                                if db == vision.enums.TextAnnotation.DetectedBreak.BreakType.LINE_BREAK:
                                    new_word = new_word + '\n'
                                else:
                                    new_word = new_word + ' '

                        paragraph_text = paragraph_text + new_word

                    paragraphs_with_boundaries['paragraphs'].append({
                        'boundingBox': paragraph_boundary,
                        'text': paragraph_text
                    })

        return paragraphs_with_boundaries
