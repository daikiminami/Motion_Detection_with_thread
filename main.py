import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'model/PyTorch-YOLOv3/'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'deepsort/'))

import concurrent.futures
import queue
import time
import cv2

from cap_data import CapData
import torch
import matplotlib.pyplot as plt
import numpy as np
import random

from pytorchyolo import detect, models
from pytorchyolo.utils.utils import load_classes
from deep_sort.utils.parser import get_config
from deep_sort.deep_sort import DeepSort

queue = queue.Queue()

model = models.load_model(
  "model/PyTorch-YOLOv3/config/yolov3.cfg",
  "model/PyTorch-YOLOv3/yolov3.weights")

def main(argc, argv):

    # 動画像の取得処理
    cap_data = CapData(argc - 1, argv[1:])
    cap_data.cap_function(queue)

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter('video.mp4',fourcc, 30.0, (1920, 1080))
    classes = load_classes('model/PyTorch-YOLOv3/data/coco.names')

    cfg = get_config()
    config_deepsort="deepsort/deep_sort/configs/deep_sort.yaml"
    cfg.merge_from_file(config_deepsort)
    deepsort = DeepSort("osnet_ibn_x1_0_MSMT17",
                        "cpu",
                        max_dist=cfg.DEEPSORT.MAX_DIST,
                        max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                        max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                        )

    #描画画像の作成
    while queue.qsize() > 0:
      img = queue.get().img
      detections = detect.detect_image(model, img)
      outputs = deepsort.update(detections[:, :4], detections[:, 4], detections[:, 5], img)
      print(outputs)

      unique_labels = np.unique(detections[:, -1])
      n_cls_preds = len(unique_labels)
      for x1, y1 , x2, y2, conf, cls_pred in detections:
        cmap = plt.get_cmap("tab20b")
        colors = [cmap(i) for i in np.linspace(0, 1, n_cls_preds)]
        bbox_colors = random.sample(colors, n_cls_preds)

        box_w = x2 - x1
        box_h = y2 - y1

        color = bbox_colors[int(np.where(unique_labels == int(cls_pred))[0])]

        cv2.rectangle(img, (x1, y1), (x2, y2), thickness=2, color=color)
        cv2.putText(img, classes[int(cls_pred)], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)


      #   # 動画の作成
      cv2.imshow('test', img)
      video.write(img)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    video.release()

if __name__ == '__main__':
    argv = sys.argv
    print('Start main')
    main(len(argv), argv)
    print('End main')