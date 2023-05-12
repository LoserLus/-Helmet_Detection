import cv2
import torch
from PIL import Image
from SORT import Sort

class Detector:
    def __init__(self):
        self.model = 'F:\Desktop\models\yolov5s_best.pt'
        self.inference = torch.hub.load('E:\Yolo5\yolov5', 'custom', path=self.model,source='local')
        self.tracker = Sort()
        # self.inference = torch.load(self.model)

    def getInferResultFromPath(self, imgPath):
        # img = Image.open(imgPath)
        result = self.inference(imgPath, size=640)
        return result
    def getInferResultFromImage(self, img):
        result = self.inference(img)
        return result
    def changeModel(self, newModel):
        self.model = newModel
        self.inference = torch.load(self.model)
    def getTrackingResult(self,img):
        result = self.getInferResultFromImage(img)
        det = result.xyxy[0]
        # print(det.cpu())
        det = det.cpu().numpy()
        # print(det)
        trackResult = self.tracker.update(det)
        return trackResult
        # print(trackResult)
        # for info in trackResult:
        #     cv2.rectangle(img, (info[1], info[2]), (info[3], info[4]), (255, 0, 0), thickness=2)
        #     cv2.putText(image, info[0], (info[1], info[2]), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 2)

