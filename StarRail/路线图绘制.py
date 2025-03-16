import json
import os

import cv2
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsView,
                               QGraphicsScene, QFileDialog, QGraphicsLineItem, QLabel, QFrame, QSizePolicy,
                               QGraphicsEllipseItem, QGraphicsSimpleTextItem, QComboBox, QCheckBox, QFormLayout,
                               QSplitter)
from PySide6.QtCore import Qt, QPoint, QTimer, Signal, QObject
from PySide6.QtGui import QImage, QPixmap, QPen, QColor, QPainter, QFont, QBrush


class CustomGraphicsView(QGraphicsView):
    def __init__(self, main_win):
        super().__init__()
        self.main_win = main_win
        self.dragging = False
        self.last_pos = QPoint()
        self.setRenderHint(QPainter.Antialiasing, False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_pos = event.pos()
            self.dragging = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if not self.dragging:
                delta = event.pos() - self.last_pos
                if delta.manhattanLength() > 3:
                    self.dragging = True
                    self.setCursor(Qt.ClosedHandCursor)
            if self.dragging:
                delta = event.pos() - self.last_pos
                self.last_pos = event.pos()
                h_bar = self.horizontalScrollBar()
                v_bar = self.verticalScrollBar()
                h_bar.setValue(h_bar.value() - delta.x())
                v_bar.setValue(v_bar.value() - delta.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.dragging:
                self.setCursor(Qt.ArrowCursor)
            else:
                scene_pos = self.mapToScene(event.pos())
                if self.main_win.image_item:
                    img = self.main_win.image_item.pixmap()
                    if (0 <= scene_pos.x() < img.width() and
                            0 <= scene_pos.y() < img.height()):
                        self.main_win.add_point(scene_pos.x(), scene_pos.y())
            self.dragging = False
            self.last_pos = QPoint()
        super().mouseReleaseEvent(event)


class MessageFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.hide)

    def setup_ui(self):
        self.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px;
        """)
        layout = QHBoxLayout()
        self.label = QLabel("保存成功！")
        close_btn = QPushButton("×")
        close_btn.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                font-size: 16px;
                padding: 0 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.hide)

        layout.addWidget(self.label)
        layout.addWidget(close_btn)
        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.timer.start(3000)  # 3秒后自动隐藏


# 新增类定义
class PointSignals(QObject):
    selected = Signal(int)
    hovered = Signal(int)


class AnnotationPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.move_type = ""
        self.stop_after_arrival = False
        self.check_position = False
        self.use_skill = False
        self.normal_attack = False


class PointMarker(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, point_id, signals):
        super().__init__(x - radius, y - radius, radius * 2, radius * 2)
        self.point_id = point_id
        self.signals = signals
        self.normal_radius = radius
        self.setPen(QPen(QColor(255, 0, 0)))
        self.setBrush(QBrush(Qt.white))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setRect(self.rect().adjusted(-2, -2, 2, 2))  # 放大效果
        self.signals.hovered.emit(self.point_id)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setRect(self.rect().adjusted(2, 2, -2, -2))
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        self.signals.selected.emit(self.point_id)
        super().mousePressEvent(event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Marker")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 按钮布局
        btn_layout = QHBoxLayout()
        self.btn_open = QPushButton("打开地图文件")
        self.btn_undo = QPushButton("撤回最后一个点位")
        self.btn_save = QPushButton("保存路线")

        btn_layout.addWidget(self.btn_open)
        btn_layout.addWidget(self.btn_undo)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

        # 图形视图和场景
        self.scene = QGraphicsScene()
        self.view = CustomGraphicsView(self)
        self.view.setScene(self.scene)
        layout.addWidget(self.view)

        # 初始化变量
        self.image_item = None
        self.points = []  # 存储坐标点
        self.points_items = []  # 存储点的图形项
        self.lines = []  # 存储连接线
        # 新增用于存储当前图片路径的变量
        self.current_image_path = ""

        # 连接信号
        self.btn_open.clicked.connect(self.open_image)
        self.btn_undo.clicked.connect(self.undo_last_point)
        self.btn_save.clicked.connect(self.save_annotations)

        # 调整按钮样式
        button_style = """
                    QPushButton {
                        min-height: 40px;
                        font-size: 14px;
                        padding: 10px;
                    }
                """
        for btn in [self.btn_open, self.btn_undo, self.btn_save]:
            btn.setStyleSheet(button_style)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 创建消息框
        self.msg_frame = MessageFrame(self)
        self.msg_frame.hide()

        # 新增右侧面板
        self.splitter = QSplitter(Qt.Horizontal)
        self.right_panel = QFrame()
        self.right_panel.setFixedWidth(300)
        self.setup_right_panel()

        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.right_panel)
        layout.addWidget(self.splitter)

        # 新增信号和状态
        self.signals = PointSignals()
        self.signals.selected.connect(self.on_point_selected)
        self.current_point = None
        # self.points = []  # 替换原有points_coords

    def setup_right_panel(self):
        layout = QVBoxLayout()
        self.right_panel.setLayout(layout)

        # 详情表单
        self.detail_form = QFormLayout()
        self.move_combo = QComboBox()
        self.move_combo.addItems(["", "walk", "run"])
        self.stop_check = QCheckBox()
        self.check_check = QCheckBox()
        self.skill_check = QCheckBox()
        self.attack_check = QCheckBox()

        self.detail_form.addRow("移动方式:", self.move_combo)
        self.detail_form.addRow("到达停止:", self.stop_check)
        self.detail_form.addRow("检测坐标:", self.check_check)
        self.detail_form.addRow("使用技能:", self.skill_check)
        self.detail_form.addRow("普通攻击:", self.attack_check)

        # 保存按钮
        self.save_btn = QPushButton("保存当前点位设置")
        self.save_btn.clicked.connect(self.save_point_settings)

        layout.addLayout(self.detail_form)
        layout.addWidget(self.save_btn)
        self.right_panel.hide()

    def show_save_message(self):
        # 计算居中位置
        x = (self.width() - self.msg_frame.width()) // 2
        y = 10  # 显示在顶部
        self.msg_frame.move(x, y)
        self.msg_frame.show()

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.current_image_path = file_path  # 存储当前路径
            img = cv2.imread(file_path)
            if img is not None:
                # 转换颜色空间 BGR -> RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, ch = img.shape
                bytes_per_line = ch * w
                q_img = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)

                # 清除旧数据
                self.scene.clear()
                self.points.clear()
                self.points_items.clear()
                self.lines.clear()

                # 添加新图像
                self.image_item = self.scene.addPixmap(pixmap)
                self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
                self.view.resetTransform()

                # 新增JSON加载逻辑
                json_path = os.path.splitext(file_path)[0] + '.json'
                if os.path.exists(json_path):
                    try:
                        with open(json_path, 'r') as f:
                            data = json.load(f)
                            for pid, pdata in sorted(data.items(), key=lambda x: int(x[0])):
                                x = pdata['x']
                                y = pdata['y']
                                self.add_point(x, y)

                                point = self.points[-1]
                                point.move_type = pdata.get('move_type', '')
                                point.stop_after_arrival = pdata.get('stop_after_arrival', False)
                                point.check_position = pdata.get('check_position', False)
                                point.use_skill = pdata.get('use_skill', False)
                                point.normal_attack = pdata.get('normal_attack', False)
                    except Exception as e:
                        print(f"加载标注失败: {e}")

    def add_point(self, x, y):
        # 创建数据对象
        point = AnnotationPoint(x, y)
        self.points.append(point)

        # 创建图形项
        radius = 10
        marker = PointMarker(x, y, radius, len(self.points) - 1, self.signals)
        text = QGraphicsSimpleTextItem(str(len(self.points)))
        text.setFont(QFont("Arial", 8, QFont.Bold))
        text.setPos(x - text.boundingRect().width() / 2,
                    y - text.boundingRect().height() / 2)

        self.scene.addItem(marker)
        self.scene.addItem(text)

        # 保存图形项引用
        self.points_items.append({
            "marker": marker,
            "text": text
        })

        # 创建连接线（保持原有绿色直线逻辑）
        if len(self.points) >= 2:
            prev_point = self.points[-2]
            prev_x = prev_point.x
            prev_y = prev_point.y
            line = QGraphicsLineItem(prev_x, prev_y, x, y)
            line.setPen(QPen(QColor(0, 255, 0)))
            self.scene.addItem(line)
            self.lines.append(line)

    def on_point_selected(self, index):
        self.current_point = index
        point = self.points[index]

        # 更新表单
        self.move_combo.setCurrentText(point.move_type)
        self.stop_check.setChecked(point.stop_after_arrival)
        self.check_check.setChecked(point.check_position)
        self.skill_check.setChecked(point.use_skill)
        self.attack_check.setChecked(point.normal_attack)

        self.right_panel.show()

    def save_point_settings(self):
        if self.current_point is None:
            return

        point = self.points[self.current_point]
        point.move_type = self.move_combo.currentText()
        point.stop_after_arrival = self.stop_check.isChecked()
        point.check_position = self.check_check.isChecked()
        point.use_skill = self.skill_check.isChecked()
        point.normal_attack = self.attack_check.isChecked()

        self.save_annotations()

    def undo_last_point(self):
        if not self.points:
            return

        # 移除最后一个点
        self.points.pop()
        last_items = self.points_items.pop()

        # 移除图形项
        self.scene.removeItem(last_items["marker"])
        self.scene.removeItem(last_items["text"])

        # 移除对应的连接线
        if self.lines:
            last_line = self.lines.pop()
            self.scene.removeItem(last_line)

        # 自动更新剩余点编号
        for i, item in enumerate(self.points_items):
            item["text"].setText(str(i + 1))

    def save_annotations(self):
        if not self.current_image_path or not self.points:
            return

        # 构建保存路径
        json_path = os.path.splitext(self.current_image_path)[0] + '.json'

        # 构建数据结构
        data = {
            str(i + 1): {
                "x": p.x,
                "y": p.y,
                "move_type": p.move_type,
                "stop_after_arrival": p.stop_after_arrival,
                "check_position": p.check_position,
                "use_skill": p.use_skill,
                "normal_attack": p.normal_attack
            } for i, p in enumerate(self.points)
        }

        # 写入文件
        try:
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=4)
            self.show_save_message()  # 显示保存提示
        except Exception as e:
            print(f"保存失败: {e}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec()
