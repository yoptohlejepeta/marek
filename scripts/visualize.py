import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

COLORS = ["red", "green", "blue", "yellow", "magenta"]


def visualize(npy_path: str):
    data = np.load(npy_path, allow_pickle=True).item()
    image_path = data["image_path"]
    objects = data["objects"]

    img = plt.imread(image_path)

    plt.figure(figsize=(img.shape[1] / 100, img.shape[0] / 100), dpi=100)
    plt.imshow(img)

    for i, polygon_points in enumerate(objects):
        color = COLORS[i % len(COLORS)]
        polygon = Polygon(polygon_points, fill=True, facecolor=color, alpha=0.3, edgecolor=color, linewidth=2)
        plt.gca().add_patch(polygon)

    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <path_to_npy>")
        sys.exit(1)

    visualize(sys.argv[1])
