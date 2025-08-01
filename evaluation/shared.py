from typing import List
from memory_manager.observable_unit_tools.handlers.dfr_observable_unit_handler import DfrObservableUnitHandler
from memory_manager.observable_unit_tools.handlers.event_observable_unit_handler import EventObservableUnitHandler
from memory_manager.observable_unit_tools.handlers.trace_observable_unit_handler import TraceObservableUnitHandler
from memory_manager.observable_unit_tools.handlers.variant_observable_unit_handler import VariantObservableUnitHandler
from memory_manager.policies.exponential_decay_counting_policy import ExponentialDecayCountingPolicy
from memory_manager.policies.lossy_count_with_budget_policy import LossyCountWithBudgetPolicy
from memory_manager.policies.reservoir_sampling_policy import ReservoirSamplingPolicy
from memory_manager.policies.sliding_window_policy import SlidingWindowPolicy
from memory_manager.policies.tumbling_window_policy import TumblingWindowPolicy

import seaborn as sns
import pandas as pd
import os

import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt

class EvalData:
    def __init__(self):
        self.event_counter = 0
        self.processing_times = []
        self.memory_footprints = []
        self.dfr_completeness = []
        self.variant_completeness = []
        self.activity_completeness = []

    def clear(self):
        self.event_counter = 0
        self.processing_times = []
        self.memory_footprints = []
        self.dfr_completeness = []

    def avg_processing_time(self):
        return sum(self.processing_times) / len(self.processing_times)

    def avg_memory_footprint(self):
        return sum(self.memory_footprints) / len(self.memory_footprints)

def plot_line_chart(data: List[float], title: str = "Line Chart", xlabel: str = "Events", ylabel: str = "Completeness", fig_name = "fig.png"):
    plt.figure(figsize=(16, 6))
    plt.plot(data, marker='', linewidth=1.5)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/" + fig_name, dpi=300)

def plot_line_chart_multiple_lines(data_set: List[tuple[str, list]], title: str = "Line Chart", xlabel: str = "Events", ylabel: str = "Completeness", path: str = "evaluation/results/"):
    plt.figure(figsize=(16, 6))

    for data in data_set:
        plt.plot(data[1], label=data[0], marker='', linewidth=1.5)

    plt.legend()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plot_name = title.replace(" ", "_") + ".png"
    plt.savefig(path + plot_name, dpi=300)

def plot_table(title: str, data: [], rows: [], columns: []):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')

    # Create the table
    table = ax.table(
        cellText=data,
        rowLabels=rows,
        colLabels=columns,
        loc='center',
        cellLoc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)  # Adjust row height

    plt.title(title, fontsize=14, pad=20)
    plt.tight_layout()
    table_name = title.replace(" ", "_") + ".png"
    os.makedirs("evaluation/results", exist_ok=True)
    plt.savefig("evaluation/results/" + table_name, dpi=300)


def plot_heatmap(title: str, data: list, rows: list, columns: list):
    df = pd.DataFrame(data, index=rows, columns=columns)

    plt.figure(figsize=(7, 6))

    sns.heatmap(df, annot=True, fmt=".2f", cmap="YlGnBu", cbar=True, linewidths=.5, linecolor='gray')

    plt.title(title, fontsize=14, pad=20)
    plt.tight_layout()

    table_name = title.replace(" ", "_") + ".png"
    os.makedirs("evaluation/results", exist_ok=True)
    plt.savefig("evaluation/results/" + table_name, dpi=300)

policies = {

    "SW20": SlidingWindowPolicy(20),
    "EDC20": ExponentialDecayCountingPolicy(20),
    "LCB20": LossyCountWithBudgetPolicy(20),
    "RS20": ReservoirSamplingPolicy(20),
    "TW20": TumblingWindowPolicy(20),

    "SW10": SlidingWindowPolicy(10),
    "EDC10": ExponentialDecayCountingPolicy(10),
    "LCB10": LossyCountWithBudgetPolicy(10),
    "RS10": ReservoirSamplingPolicy(10),
    "TW10": TumblingWindowPolicy(10),

    "SW5": SlidingWindowPolicy(5),
    "EDC5": ExponentialDecayCountingPolicy(5),
    "LCB5": LossyCountWithBudgetPolicy(5),
    "RS5": ReservoirSamplingPolicy(5),
    "TW5": TumblingWindowPolicy(5),

}

observable_units_handlers = {
    "event": EventObservableUnitHandler(),
    "DFR": DfrObservableUnitHandler(),
    "variant": VariantObservableUnitHandler(),
    "trace": TraceObservableUnitHandler(),
}