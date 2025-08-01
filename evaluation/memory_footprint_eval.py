from typing import List
import copy

from pybeamline.bevent import BEvent
from pybeamline.sources import xes_log_source_from_file
from pympler import asizeof

from evaluation.shared import EvalData, policies, observable_units_handlers, plot_heatmap
from memory_manager.manager import MemoryManager


def handle(e: BEvent, data: EvalData):
    data.event_counter += 1
    mm.add_event(e)
    data.memory_footprints.append(asizeof.asizeof(mm))

result = {}
log: List[BEvent] = []
xes_log_source_from_file("Log_Supply_steady.xes").subscribe(lambda x: log.append(x))

log = log[:1000]
for policy_key in policies:
    result[policy_key] = {}
    for ouh_key in observable_units_handlers:
        eval_data = EvalData()
        print("Memory footprint test started. Policy -> ", policy_key, ". Observable Uint -> ", ouh_key)
        policy_copy = copy.deepcopy(policies[policy_key])
        mm = MemoryManager(policy_copy, observable_units_handlers[ouh_key])
        for event in log:
            handle(event, eval_data)
        print("Memory footprint test ended. Policy -> ", policy_key, ". Observable Uint -> ", ouh_key)
        result[policy_key][ouh_key] = eval_data

mf_columns = list(observable_units_handlers.keys())
mf_rows = list(policies.keys())

cell_text = []
cell_num = []
for policy_key in mf_rows:
    row = []
    num_row = []
    for ouh_key in mf_columns:
        eval_data = result[policy_key][ouh_key]
        avg_mem = eval_data.avg_memory_footprint() if eval_data.memory_footprints else 0
        num_row.append(avg_mem/1000)
        row.append(f"{avg_mem/1000:.0f}")
    cell_text.append(row)
    cell_num.append(num_row)

plot_heatmap("Average Memory footprint (kB)", cell_num, mf_rows, mf_columns)
