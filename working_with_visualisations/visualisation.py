import pandas as pd
from matplotlib import pyplot as plt


def show_lab_hours(data: pd.DataFrame, column):
    try:
        x = data[column].values.tolist()
        y = data["Всего человеко часов"].values.tolist()
        plt.plot(x, y, color="green", linewidth=3, marker="o", markersize=15, linestyle="--")
        plt.title("Total labor hours")
        plt.xlabel(column)
        plt.ylabel("Всего человеко часов")
        plt.show()
    except KeyError:
        print("No such column un the data.")


def show_mach_hours(data: pd.DataFrame, column):
    try:
        x = data[column].values.tolist()
        y = data["Всего машино часов"].values.tolist()
        plt.plot(x, y, color="green", linewidth=3, marker="o", markersize=15, linestyle="--")
        plt.title("Total labor hours")
        plt.xlabel(column)
        plt.ylabel("Всего машино часов")
        plt.show()
    except KeyError:
        print("No such column in the data.")
