import tensorrt as trt
from jetbot.ssd_tensorrt import load_plugins, parse_boxes, TRT_INPUT_NAME, TRT_OUTPUT_NAME
#from .tensorrt_model import TRTModel
import numpy as np
import cv2

print("in object detector")

logger = trt.Logger()

trt.init_libnvinfer_plugins(logger, '')

load_plugins()

runtime = trt.Runtime(logger)

with open('ssd_mobilenet_v2_v04_coco.engine', 'rb') as f:
    engine = runtime.deserialize_cuda_engine(f.read())

print("engine opened")
