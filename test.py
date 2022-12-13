# -*- coding: utf-8 -*-
#import models
from models.model_detector import ObjDetector

if __name__ == '__main__':
	#print(ObjDetector)
	detector = ObjDetector()
	detector.loadModels()
	detector.startCapture()
