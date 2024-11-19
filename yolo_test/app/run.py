import os
import random
import uuid

from flask import Flask, render_template, request, jsonify, send_from_directory
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

# 用于存储处理后的图像
OUTPUT_DIR = 'output_images'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# 加载模型的函数
def load_model(model_type):
    if model_type == 'seg':
        return YOLO('yolov8n-seg.pt')
    elif model_type == 'pose':
        return YOLO('yolov8n-pose.pt')
    else:
        return YOLO('yolov8n.pt')


def yolov8_predict(image, model_type='detect'):
    model = load_model(model_type)

    output_image_filename = f'processed_image_{model_type}_{str(uuid.uuid4())}.jpg'
    output_image_path = os.path.join(OUTPUT_DIR, output_image_filename)

    # 检测、分割任务
    if model_type in ['detect', 'seg', 'pose']:
        results = model.predict(source=image, show=False, save=False)
    elif model_type == 'track':
        # 跟踪任务
        results = model.track(source=image, show=False, save=False)
        processed_image = image  # 对于跟踪，通常是视频帧，没有处理后的图像
    else:
        return [], None  # 如果任务类型不匹配，返回空

    detections = []

    for result in results:
        if hasattr(result, 'boxes'):
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                detections.append({
                    'box': [x1, y1, x2, y2],
                    'confidence': float(conf),
                    'class_id': cls
                })

                # 在图像上绘制边界框
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                label = f'Class {cls}: {conf:.2f}'
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # 处理后的图像保存
    cv2.imwrite(output_image_path, image)

    return detections, output_image_filename



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'images' not in request.files:
        return jsonify({'error': 'No images provided'}), 400

    files = request.files.getlist('images')
    if not files:
        return jsonify({'error': 'No image files selected'}), 400

    task_type = request.form.get('task_type', 'detect')
    results = []

    # 对于多张图片处理，每张图片生成单独的处理结果
    for idx, file in enumerate(files):
        img_stream = file.read()
        image = cv2.imdecode(np.frombuffer(img_stream, np.uint8), cv2.IMREAD_COLOR)

        # 进行预测
        predictions, processed_image_filename = yolov8_predict(image, model_type=task_type)
        print(f'Processed image saved to {processed_image_filename}')
        results.append({
            'predictions': predictions,
            'processed_image': processed_image_filename
        })

    return render_template('results.html', results=results)


@app.route('/output_images/<filename>')
def send_image(filename):
    return send_from_directory(OUTPUT_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True)
