import copy
import statistics

from collections import defaultdict

from pybeamline.bevent import BEvent
from pybeamline.sources import xes_log_source_from_file

from evaluation.shared import policies, observable_units_handlers, EvalData, plot_table, plot_line_chart_multiple_lines, \
    plot_heatmap
from memory_manager.manager import MemoryManager


def extract_traces(events: list[BEvent]) -> dict[str, list[BEvent]]:
    traces = defaultdict(list)
    for event in events:
        traces[event.get_trace_name()].append(event)
    return traces

def extract_dfrs(traces: dict[str, list[BEvent]]) -> set[tuple[str, str]]:
    dfrs = set()
    for trace in traces.values():
        if len(trace) > 1:
            for i in range(len(trace) - 1):
                a1 = trace[i].get_event_name()
                a2 = trace[i + 1].get_event_name()
                dfrs.add((a1, a2))
    return dfrs

def extract_variants(traces: dict[str, list[BEvent]]):
    variants = set()
    for trace in traces.values():
        variant = tuple(event.get_event_name() for event in trace)
        variants.add(variant)
    return variants

def extract_activities(events: list[BEvent]) -> set[str]:
    return {e.get_event_name() for e in events}

def calculate_dfr_completeness(current_dfrs: set, base_dfrs: set) -> float:
    return calculate_jaccard_similarity(current_dfrs, base_dfrs)

def calculate_activity_completeness(current_activities: set, base_activities: set) -> float:
   return calculate_jaccard_similarity(current_activities, base_activities)

def calculate_variant_completeness(current_variants: set, base_variants: set) -> float:
    return calculate_jaccard_similarity(current_variants, base_variants)

def calculate_jaccard_similarity(current: set[str], base: set[str]) -> float:
    intersection = base.intersection(current)
    union = base.union(current)
    if not union:
        return 1.0
    return len(intersection) / len(union)

def  eval_event(e: BEvent, data: EvalData, l: list[BEvent], memory_manager: MemoryManager):
    data.event_counter += 1
    memory_manager.add_event(e)

    log_traces = extract_traces(l[:data.event_counter])
    manager_traces = extract_traces(memory_manager.get_data())

    log_variants = extract_variants(log_traces)
    manager_variants = extract_variants(manager_traces)
    data.variant_completeness.append(calculate_variant_completeness(manager_variants, log_variants))

    log_activities = extract_activities(l[:data.event_counter])
    manager_activities = extract_activities(memory_manager.get_data())
    data.activity_completeness.append(calculate_activity_completeness(manager_activities, log_activities))

    log_dfrs = extract_dfrs(log_traces)
    manager_dfrs = extract_dfrs(manager_traces)
    data.dfr_completeness.append(calculate_dfr_completeness(manager_dfrs, log_dfrs))


def run_eval(file: str, event_num: int, drift_indexes: []):
    log: list[BEvent] = []
    xes_log_source_from_file(file).subscribe(lambda x: log.append(x))

    drift_logs = []

    for i in range(len(drift_indexes) - 1):
        drift_log = log[drift_indexes[i]:drift_indexes[i + 1]]
        drift_log = drift_log[:event_num]
        drift_logs.append(drift_log)

    log = log[:event_num]

    steady_result = {}

    for policy_key in policies:
        steady_result[policy_key] = {}
        for ouh_key in observable_units_handlers:
            eval_data = EvalData()
            print("Test started. Policy: ", policy_key, " Observable uint: ", ouh_key)
            policy_copy = copy.deepcopy(policies[policy_key])
            mm = MemoryManager(policy_copy, observable_units_handlers[ouh_key])
            if not drift_indexes:
                for event in log:
                    eval_event(event, eval_data, log, mm)
            else:
                for drift_log in drift_logs:
                    eval_data.event_counter = 0
                    for event in drift_log:
                        eval_event(event, eval_data, drift_log, mm)
            steady_result[policy_key][ouh_key] = eval_data

    columns = list(observable_units_handlers.keys())
    num_cell_dfr = []
    num_cell_variant = []
    rows = list(policies.keys())
    cell_text = []
    for policy_key in rows:
        row = []
        num_row_dfr = []
        num_row_variant = []
        for ouh_key in columns:
            eval_data: EvalData = steady_result[policy_key][ouh_key]
            deviation = statistics.stdev(eval_data.dfr_completeness)
            avg = statistics.mean(eval_data.dfr_completeness)
            row.append(f"{avg:.3f}" + " | " + f"{deviation:.3f}")
            num_row_dfr.append(avg)
            avg_variant = statistics.mean(eval_data.variant_completeness)
            num_row_variant.append(avg_variant)
        cell_text.append(row)
        num_cell_dfr.append(num_row_dfr)
        num_cell_variant.append(num_row_variant)

    if len(drift_indexes) > 0:
        plot_table("DFR average completeness and deviation drift", cell_text, rows, columns)
        plot_heatmap("DFR average completeness heatmap drift", num_cell_dfr, rows, columns)
        plot_heatmap("Variant avg completeness heatmap drift", num_cell_variant, rows, columns)
    else:
        plot_table("DFR average completeness and deviation", cell_text, rows, columns)
        plot_heatmap("DFR average completeness heatmap", num_cell_dfr, rows, columns)
        plot_heatmap("Variant avg completeness heatmap", num_cell_variant, rows, columns)

    for policy_key in rows:
        data_pack_dfr = []
        data_pack_activities = []
        data_pack_variants = []
        for ouh_key in columns:
            eval_data: EvalData = steady_result[policy_key][ouh_key]
            data_pack_dfr.append((ouh_key, eval_data.dfr_completeness))
            data_pack_activities.append((ouh_key, eval_data.activity_completeness))
            data_pack_variants.append((ouh_key, eval_data.variant_completeness))

        path = "evaluation/results/steady/" if not drift_indexes else "evaluation/results/drift/"
        plot_line_chart_multiple_lines(data_pack_dfr, "DFR completeness " + policy_key, path = path)
        plot_line_chart_multiple_lines(data_pack_variants, "Variant completeness " + policy_key,  path = path)
        plot_line_chart_multiple_lines(data_pack_activities, "Activity completeness " + policy_key,  path = path)

run_eval("Log_Supply_steady.xes", 1000, [])






