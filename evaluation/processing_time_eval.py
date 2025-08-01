import time
from typing import List
import copy

from pybeamline.bevent import BEvent
from pybeamline.sources import xes_log_source_from_file

from evaluation.shared import EvalData, policies, observable_units_handlers, plot_table, plot_heatmap
from memory_manager.manager import MemoryManager


def handle(e: BEvent, data: EvalData):
    data.event_counter += 1
    start_time = time.perf_counter()
    mm.add_event(e)
    end_time = time.perf_counter()
    e = mm.get_data()
    data.processing_times.append(end_time - start_time)


result = {}
log: List[BEvent] = []
xes_log_source_from_file("Log_Supply_steady.xes").subscribe(lambda x: log.append(x))
log = log[:1000]

for policy_key in policies:
    result[policy_key] = {}
    for ouh_key in observable_units_handlers:
        eval_data = EvalData()
        print("Processing time test started. Policy -> ", policy_key, ". Observable Uint -> ", ouh_key)
        policy_copy = copy.deepcopy(policies[policy_key])
        mm = MemoryManager(policy_copy, observable_units_handlers[ouh_key])
        for event in log:
            handle(event, eval_data)
        print("Processing time test ended. Policy -> ", policy_key, ". Observable Uint -> ", ouh_key)
        result[policy_key][ouh_key] = eval_data

pt_columns = list(observable_units_handlers.keys())
pt_rows = list(policies.keys())

cell_text = []
cell_num = []
for policy_key in pt_rows:
    row = []
    num_row = []
    for ouh_key in pt_columns:
        eval_data = result[policy_key][ouh_key]
        avg_time = eval_data.avg_processing_time() if eval_data.processing_times else 0
        row.append(f"{avg_time * 1000:.6f}")
        num_row.append(avg_time * 100000)
    cell_text.append(row)
    cell_num.append(num_row)

plot_heatmap("Average Processing Time (µs)", cell_num, pt_rows, pt_columns)