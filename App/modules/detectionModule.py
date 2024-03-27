from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Suppressing the logging output of transformers
import logging


class Detector:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.initModel()

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

        text = ImageCropper.textEditAIText.toPlainText()
        paragraphs = text.split('\n')
        paragraphs = [para for para in paragraphs if para.strip() != '']
        results = []
        for para in paragraphs:
            result = self._detect(para)
            results.append(result)
            hover_text = f"Detection Result: {result['type']}, Level: {result['lvl']}"
        ImageCropper.detectResultContent.reloadContent(results)
        ImageCropper.textEditAIText.setDisabled(False)
        ImageCropper.buttonFromOCR.setDisabled(False)
        ImageCropper.buttonAIStart.setDisabled(False)
        ImageCropper.buttonReloadModel.setDisabled(False)

    def _detect(self, para) -> dict:
        # Tokenize the input text and convert to Tensor
        dic = {'text': para}
        inputs = self.tokenizer(para, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        prob = torch.nn.functional.softmax(logits, dim=1)
        human = prob[0][0].item() * 100
        gpt = prob[0][1].item() * 100
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
