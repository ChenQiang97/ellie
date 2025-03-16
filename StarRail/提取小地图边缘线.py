import cv2
import numpy as np

if __name__ == '__main__':
    image = cv2.imread(r'D:\workspace\StarRailAuto\StarRailOneDragon-main\test\img.png')
    mini_info = analyse_mini_map(cut_mini_map(image, MiniMapPos(140, 151, 94.00)))
    cv2.imshow('mini_map', mini_info.raw)

    l1 = 170
    u1 = 250
    lower_color = np.array([l1, l1, l1], dtype=np.uint8)
    upper_color = np.array([u1, u1, u1], dtype=np.uint8)
    road_mask = cv2.inRange(mini_info.raw, lower_color, upper_color)

    # 非道路连通块 < 50的(小的黑色块) 认为是噪点 加入道路
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(road_mask, connectivity=4)
    large_components = []
    for label in range(1, num_labels):
        if stats[label, cv2.CC_STAT_AREA] < 100:
            large_components.append(label)
    for label in large_components:
        road_mask[labels == label] = 0

    road_mask = cv2.bitwise_and(road_mask, mini_info.circle_mask)
    cv2.imshow('road_mask', road_mask)

    # 使用形态学操作连接断断续续的白色线条
    kernel = np.ones((2,2), np.uint8)  # 你可以根据需要调整kernel的大小
    road_mask = cv2.dilate(road_mask, kernel, iterations=1)

    # 定义边框的颜色为白色
    border_color = (255, 255, 255)

    # 定义边框的宽度
    border_thickness = 2

    # 计算圆的中心坐标
    center_coordinates = (road_mask.shape[1] // 2, road_mask.shape[0] // 2)

    # 计算圆的半径
    radius = int(road_mask.shape[0] // 2) - 20

    # 在mask图中绘制圆形边框
    cv2.circle(road_mask, center_coordinates, radius, border_color, border_thickness)

    # 创建一个新的掩码图像
    result_mask = np.zeros_like(road_mask)

    # 找到中心点
    center_x = road_mask.shape[1] // 2
    center_y = road_mask.shape[0] // 2

    # 与中心点相连的连通区域
    _, center_labels, _, _ = cv2.connectedComponentsWithStats(road_mask, connectivity=4)
    center_label = center_labels[center_y, center_x]
    # 将与中心点相连的区域填充为白色
    result_mask[center_labels == center_label] = 255

    cv2.imshow('Connected road_mask_1', road_mask)
    cv2.imshow('Result Mask', result_mask)

    # # 显示结果
    # cv2.imshow('lm_image', lm_image)
    cv2.waitKey()
    cv2.destroyAllWindows()