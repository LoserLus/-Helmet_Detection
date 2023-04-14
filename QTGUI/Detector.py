import torch
from PIL import Image


class Detector:
    def __init__(self):
        self.model = 'F:\Desktop\models\yolov5s_best.pt'
        self.inference = torch.hub.load('E:\Yolo5\yolov5', 'custom', path=self.model,source='local')

        # self.inference = torch.load(self.model)

    def getInferResult(self, imgPath):
        # img = Image.open(imgPath)
        result = self.inference(imgPath, size=640)
        return result

    def changeModel(self, newModel):
        self.model = newModel
        self.inference = torch.load(self.model)
