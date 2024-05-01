from PyQt5.QtCore import QThread, pyqtSignal
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Suppressing the logging output of transformers
import logging


class DetectThread(QThread):
    finished = pyqtSignal(str, bool)

    def __init__(self, detector, parent=None):
        super().__init__(parent)
        self.detector = detector
        self.text = ""
        self.errorFlag = False

    def run(self):
        print("DetectThread started")
        try:
            self.detector.initModel()
        except Exception:
            self.detector.initState = False
            self.text = f"Failed to load model.."
            self.errorFlag = True
        if self.detector.initState:
            self.text = f"Model loaded successfully!"
            self.errorFlag = False
        self.finished.emit(self.text, self.errorFlag)


class Detector:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.initState = None
        self.data = []

    def initModel(self):
        logging.getLogger("transformers").setLevel(logging.ERROR)
        logging.basicConfig(level=logging.ERROR)
        # Initialize the model and tokenizer
        model_name = "Hello-SimpleAI/chatgpt-detector-roberta"
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def startAIDetector(self, ImageCropper):
        ImageCropper.textEditAIText.setDisabled(True)
        ImageCropper.buttonFromOCR.setDisabled(True)
        ImageCropper.buttonAIStart.setDisabled(True)
        ImageCropper.buttonReloadModel.setDisabled(True)
        ImageCropper.detectResultLabel.clear()
        ImageCropper.detectResultLabel.setText("Detecting...")

        text = ImageCropper.textEditAIText.toPlainText()
        if text:
            paragraphs = text.split('\n')
            paragraphs = [para for para in paragraphs if para.strip() != '']
            results = []
            self.data = []
            for para in paragraphs:
                prob = self._detect(para)
                self.data.append({'content': para, 'proportion': prob})
                result = self.formatResult(para, prob)
                results.append(result)
            ImageCropper.detectResultContent.reloadContent(results)
            ImageCropper.detectResultLabel.clear()
        else:
            ImageCropper.detectResultLabel.setText("No text detected.")

        ImageCropper.textEditAIText.setDisabled(False)
        ImageCropper.buttonFromOCR.setDisabled(False)
        ImageCropper.buttonAIStart.setDisabled(False)
        ImageCropper.buttonReloadModel.setDisabled(False)


    def _detect(self, para) -> float:
        # Tokenize the input text and convert to Tensor

        inputs = self.tokenizer(para, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        prob = torch.nn.functional.softmax(logits, dim=1)
        return round(prob[0][0].item(), 4)

    def formatResult(self, para, prob):
        dic = {'text': para}
        human = prob * 100
        gpt = (1 - prob) * 100
        if human > gpt:
            dic['type'] = "Human"
            dic["prob"] = human
        else:
            dic['type'] = "GPT"
            dic["prob"] = gpt
        if human > 95:
            dic['lvl'] = "Highly likely human"
            dic['color'] = 'black'
        elif human > 80:
            dic['lvl'] = "Mostly human"
            dic['color'] = 'darkgray'
        elif human > 60:
            dic['lvl'] = "Possibly mixed"
            dic['color'] = 'gray'
        elif human > 40:
            dic['lvl'] = "Mostly GPT"
            dic['color'] = 'orange'
        else:
            dic['lvl'] = "Highly likely GPT"
            dic['color'] = 'red'
        return dic  # the structure of the dictionary is: {'text': '', 'prob': '', 'type': "", 'lvl': "", 'color': ''}

# if __name__ == '__main__':
#     while True:
#         print(Start())
#         print("\n")
