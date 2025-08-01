# MESS:Managing Event Stream Summaries

MESS (Managing Event Stream Summaries) is a comprehensive Python framework for streaming process mining that extracts meaningful summaries from infinite event streams.

## 🏗️ MESS Architecture

The MESS framework is built around three core components that work together to create meaningful stream summaries:

### 1. Memory Manager (`memory_manager/manager.py`)
The central orchestrator that:
- Processes streaming events immediately upon observation
- Converts events to observable units using configurable handlers
- Applies memory management policies to maintain bounded memory usage
- Handles unit merging and adaptive summarization
- Generates event log for downstream processing

### 2. Memory Management Policies (`memory_manager/policies/`)
The first hyper-parameter of MESS - five different algorithms for managing memory-constrained event streams:

- **Sliding Window (SW)**: Maintains the most recent N events using FIFO strategy
- **Tumbling Window (TW)**: Processes events in fixed-size batches with periodic resets
- **Reservoir Sampling (RS)**: Maintains a uniform random sample with probabilistic guarantees
- **Lossy Counting with Budget (LCB)**: Frequency-based sampling with bounded memory and error guarantees
- **Exponential Decay Counting (EDC)**: Time-weighted frequency counting with gradual forgetting for concept drift adaptation

### 3. Observable Unit Handlers (`memory_manager/observable_unit_tools/`)
The second hyper-parameter of MESS - handlers four different internal representations:

- **Event**: Individual process events for fine-grained analysis
- **Trace**: Complete process instances for end-to-end tracking
- **Variant**: Activity sequences representing process patterns and variants
- **DFR (Directly-Follows Relations)**: Activity transition pairs for process flow analysis

## 📊 Evaluation Framework

MESS includes a comprehensive evaluation framework in the `evaluation/` directory to validate its efficacy and applicability:

- **Completeness Evaluation**: Measures data quality retention using Jaccard similarity against complete event logs
- **Memory Footprint Analysis**: Tracks actual memory usage across different policies and observable units
- **Processing Time Analysis**: Measures per-event processing latencies for real-time performance assessment

## Getting Started with MESS

### Prerequisites

MESS is implemented as an extension to pyBeamline and requires the following dependencies:

```bash
pip install pybeamline pandas matplotlib seaborn pympler
```

### Basic Usage

```python
from memory_manager.manager import MemoryManager
from memory_manager.policies.sliding_window_policy import SlidingWindowPolicy
from memory_manager.observable_unit_tools.handlers.event_observable_unit_handler import EventObservableUnitHandler
from pybeamline.sources import xes_log_source_from_file

# Initialize MESS with chosen hyper-parameters
policy = SlidingWindowPolicy(window_size=100)  # Memory policy
handler = EventObservableUnitHandler()         # Observable unit representation
mess = MemoryManager(policy, handler)

# Process infinite event stream
log_source = xes_log_source_from_file("your_log.xes")
log_source.subscribe(lambda event: mess.add_event(event))

# Extract stream summary as event log
summary_events = mess.get_data()
# Summary can now be used with offline process mining algorithms
```

### Customizing MESS Hyper-parameters

```python
# Hyper-parameter 1: Memory Policies with different characteristics
policies = {
    "SW20": SlidingWindowPolicy(20),                    # Recent events focus
    "EDC10": ExponentialDecayCountingPolicy(10, 0.9),   # Concept drift adaptation
    "RS15": ReservoirSamplingPolicy(15),                # Uniform sampling
    "LCB25": LossyCountWithBudgetPolicy(25),            # Frequency-based retention
    "TW30": TumblingWindowPolicy(30)                    # Batch processing
}

# Hyper-parameter 2: Observable Unit Representations
handlers = {
    "event": EventObservableUnitHandler(),     # Fine-grained event analysis
    "trace": TraceObservableUnitHandler(),     # Process instance tracking  
    "variant": VariantObservableUnitHandler(), # Process pattern detection
    "dfr": DfrObservableUnitHandler()         # Process flow analysis
}

# Create MESS instance with specific configuration
mess = MemoryManager(policies["EDC10"], handlers["variant"])
```

## 📈 Running Evaluations

### Completeness Evaluation
```python
from evaluation.completeness_eval import run_eval

# Evaluate on steady-state data
run_eval("Log_Supply_steady.xes", event_num=1000, drift_indexes=[])
```

### Performance Evaluation
```python
# Memory footprint analysis
python evaluation/memory_footprint_eval.py

# Processing time analysis  
python evaluation/processing_time_eval.py
```

## 📁 Project Structure

```
├── memory_manager/
│   ├── manager.py                 # Main memory manager class
│   ├── policies/                  # Memory management policies
│   │   ├── base_policy.py
│   │   ├── sliding_window_policy.py
│   │   ├── tumbling_window_policy.py
│   │   ├── reservoir_sampling_policy.py
│   │   ├── lossy_count_with_budget_policy.py
│   │   └── exponential_decay_counting_policy.py
│   └── observable_unit_tools/     # Event representation handlers
│       ├── units/                 # Observable unit implementations
│       └── handlers/              # Conversion and merging logic
├── evaluation/                    # Evaluation framework
│   ├── completeness_eval.py       # Data quality evaluation
│   ├── memory_footprint_eval.py   # Memory usage analysis
│   ├── processing_time_eval.py    # Performance evaluation
│   └── shared.py                  # Common evaluation utilities
├── Log_Supply_steady.xes          # Sample event log (steady state)
├── Log_Supply_seasonal.xes        # Sample event log (with drift)
└── README.md
```

## 🛠️ Extensibility & Customization

MESS is designed for easy extension and customization of both hyper-parameters:

### Extending Memory Policies (Hyper-parameter 1)
1. Implement the `BasePolicy` interface
2. Define `update()`, `get_data()`, `remove_elements()`, and `get_mergeable_elements()` methods
3. Add policy-specific initialization and parameters

### Extending Observable Units (Hyper-parameter 2)  
1. **New Unit Types**: Extend `BaseObservableUnit` with domain-specific representations
2. **New Handlers**: Implement `BaseObservableUnitHandler` for conversion and merging logic
3. **Custom Merging**: Define application-specific unit combination strategies


*MESS is developed as part of streaming process mining research at DTU (Technical University of Denmark). The framework demonstrates how intelligent stream summarization can enable process mining on infinite event streams while maintaining bounded memory usage and adapting to evolving processes.*
