config_data = {
    "model-yolo-torch": {
        "_class": "vsdkx.model.yolo_torch.driver.YoloTorchDriver",
        "conf_thresh": 0.7,
        "iou_thresh": 0.4,
        "device": "cpu",
    },
    "model-yolo-tflite": {
        "_class": "vsdkx.model.yolo_tflite.driver.YoloTfliteDriver",
        "conf_thresh": 0.7,
        "iou_thresh": 0.4,
    },
    "model-yolo-facemask": {
        "_class": "vsdkx.model.yolo_facemask.driver.YoloFacemaskDriver",
        "conf_thresh": 0.7,
        "iou_thresh": 0.4,
    },
    "model-resnet": {
        "_class": "vsdkx.model.resnet.driver.ResnetDriver",
        "image_type": "BGR",
        "device": "cpu",
        "thresold": 0.16,
        "video_fps_rate": 20,
    },
    "model-mobilenet": {
        "_class": "vsdkx.model.mobilenet.driver.MobilenetDriver",
        "conf_thresh": 0.7,
        "iou_thresh": 0.4,
    },
    "model-bayesian": {
        "_class": "vsdkx.model.bayesian.driver.BayesianDriver",
        "device": "cpu",
    },
    "addon-zoning": {
        "_class": "vsdkx.addon.zoning.processor.ZoneProcessor",
        "remove_areas": [],
        "zones": [],
        "iou_thresh": (0.85,),
        "filter_class_ids": []
    },
    "addon-tracking": {
        "_class": "vsdkx.addon.tracking.processor.TrackerProcessor",
        "max_disappeared": 10,
        "distance_threshold": 500,
        "bidirectional_mode": True,
        "bidirectional_threshold": 150
    },
    "addon-distant": {
        "_class": "vsdkx.addon.distant.processor.DistanceChecker",
        "camera_distance_threshold": 0,
    },
    "addon-facemask": {
        "_class": "vsdkx.addon.facemask.processor.EntranceProcessor",
        "camera_direction": "down",
        "mask_threshold": 0.01,
        "line_border": 0.08,
    },
    "drawing": {
        "zones": [],
        "rectangle_color": (60, 179, 113),
        "text_color": (255, 255, 255),
        "text_thickness": 1,
        "text_fontscale": 1,
        "box_font_scale": 0.8,
        "box_thickness": 3,
        "zone_thickness": 3,
        "group_color": (135, 206, 235),
        "zones_color": (153, 50, 204),
    }

}
