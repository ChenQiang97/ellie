# airtest demo
import random

from airtest.core.android import Android
from airtest.core.android.touch_methods.base_touch import DownEvent, UpEvent, MoveEvent, SleepEvent
from airtest.core.api import *
import threading
import time



class SrController:
    def __init__(self):
        self.swipe_start_point = (1400, 500)
        self.finger_locks = [threading.Lock() for _ in range(5 )]
        self.device = Android(serialno='f5440073')
        self.joystick_center = (360, 650)
        self.runner_btn = (2263, 918)
        # 左滑起始点
        self.left_swipe_start_point = (1800, 500)
        # 右滑起始点
        self.light_swipe_start_point = (1000, 500)

    def start_farward(self):
        self._hold_finger(0, self.joystick_center)

    def stop_farward(self):
        self._release_finger(0, self.joystick_center)

    def switch_runner(self):
        self._hold_finger(1, self.runner_btn)
        # 此处不能释放, 会导致后续的滑动失效
        # self._release_finger(1, self.runner_btn)


    # 根据像素距离转向(滑动)
    def turn_by_pixel(self, pixel):
        # 和疾跑使用同一个手指, 否则停止前进时会失效
        self._swipe_pixel(1, pixel, steps=10, total_duration=0.8)

    def _hold_finger(self, finger_id, pos, sleep_time:float=0.0):
        with self.finger_locks[finger_id]:
            self.device.touch_proxy.base_touch.perform([
                DownEvent(self.device.touch_proxy.ori_transformer(pos), contact=finger_id, pressure=50),
                SleepEvent(sleep_time)
            ])

    def _release_finger(self, finger_id, pos):
        with self.finger_locks[finger_id]:
            self.device.touch_proxy.base_touch.perform([
                # 先按下, 再释放
                DownEvent(self.device.touch_proxy.ori_transformer(pos), contact=finger_id, pressure=50),
                UpEvent(contact=finger_id)
            ])

    def _swipe_pixel(self, finger_id, pixel, steps=10, total_duration=1.0):
        # 步数搞多点, 中间有失败也不会导致结果偏差太多
        # start = self.light_swipe_start_point if pixel > 0 else self.left_swipe_start_point
        start = self.swipe_start_point
        # Calculate the interval duration for each sleep event
        # 滑动后, 手指会复位. 所以此处的sleep缩短一些, 给手指复位留出时间
        interval_duration = total_duration / (2 * (steps - 1))

        # Calculate the increment for each move event
        increment = pixel / (steps - 1)

        swipe_event = [
            DownEvent(self.device.touch_proxy.ori_transformer(start), contact=finger_id, pressure=50)
        ]
        for i in range(steps):
            swipe_event.append(MoveEvent(self.device.touch_proxy.ori_transformer((start[0] + int(increment * (i+1)), start[1])), contact=finger_id, pressure=50)),
            swipe_event.append(SleepEvent(interval_duration))

        swipe_event.append(UpEvent(contact=finger_id))

        # 执行滑动
        with self.finger_locks[finger_id]:
            self.device.touch_proxy.base_touch.perform(swipe_event)

        # 手指复位, 将点击位置移动移动到起始位置, 防止下次滑动时从上次滑动结束点开始
        with self.finger_locks[finger_id]:
            self.device.touch_proxy.base_touch.perform([
                DownEvent(self.device.touch_proxy.ori_transformer(start), contact=finger_id, pressure=50),
                UpEvent(contact=finger_id)
            ])


if __name__ == '__main__':
    sr = SrController()
    # sr.start_farward()
    # time.sleep(1)
    # sr.switch_runner()
    # time.sleep(1)
    # for i in range(5):
    #     dis = random.choice([500, -500])
    #     print(dis)
    #     start_time = time.time()
    #     sr.turn_by_pixel(dis)
    #     end_time = time.time()
    #     print(f"turn {dis} pixel, time cost: {end_time - start_time}s")
    #     time.sleep(1)
    #
    # # sr.switch_runner()
    # # time.sleep(1)
    # for i in range(5):
    #     dis = random.choice([500, -500])
    #     print(dis)
    #     start_time = time.time()
    #     sr.turn_by_pixel(dis)
    #     end_time = time.time()
    #     print(f"turn {dis} pixel, time cost: {end_time - start_time}s")
    #     time.sleep(1)
    #
    # sr.stop_farward()

    sr._hold_finger(0, (200, 1400))
    time.sleep(1)
    sr._hold_finger(1, (400, 500))
    time.sleep(1)
    sr._hold_finger(2, (600, 500))
    time.sleep(1)
    sr._hold_finger(3, (800, 500))
    time.sleep(1)
    sr._hold_finger(4, (1000, 500))
    time.sleep(1)
    sr._release_finger(4, (100, 100))
    time.sleep(1)
    sr._release_finger(3, (100, 100))
    time.sleep(1)
    sr._release_finger(2, (100, 100))
    time.sleep(1)
    sr._release_finger(1, (100, 100))
    time.sleep(1)
    sr._release_finger(0, (100, 100))

