from math import exp
from time import time
from typing import List, override, Dict, Tuple
from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit
from memory_manager.policies.base_policy import BasePolicy

class ExponentialDecayCountingPolicy(BasePolicy):
    """
    Memory management policy that uses exponential decay to count and manage observable units.
    Older units' weights decay over time, and the policy maintains a fixed budget.
    """

    @override
    def __init__(self, budget: int, decay: float = 0.9) -> None:
        """
        Initialize the policy with a budget and decay factor.
        Args:
            budget (int): Maximum number of unique keys to keep.
            decay (float): Decay factor (between 0 and 1) for weights.
        """
        self.budget: int = budget
        self.decay: float = decay  # Decay factor: between 0 and 1
        self.data: Dict[BaseObservableUnit, Tuple[List[str], float, float]] = {}
        self.N: int = 0

    @override
    def update(self, unit: BaseObservableUnit) -> None:
        self.N += 1
        current_time = time()

        # Decay all weights based on time since last update
        for k in list(self.data.keys()):
            case_ids, weight, last_updated = self.data[k]
            dt = current_time - last_updated
            decayed_weight = weight * exp(-self.decay * dt)
            self.data[k] = (case_ids, decayed_weight, current_time if k == unit else last_updated)

        if unit in self.data:
            case_ids, weight, _ = self.data[unit]
            case_ids.append(unit.get_case_id())
            case_ids = case_ids[-self.budget:]
            self.data[unit] = (case_ids, self.data[unit][1] + 1.0, current_time)
        else:
            self.data[unit] = ([unit.get_case_id()], 1.0, current_time)

        if len(self.data) > self.budget:
            self.trim()

    def trim(self) -> None:
        current_time = time()

        # Use decayed weight for comparison
        def effective_weight(entry):
            _, weight, last_updated = self.data[entry]
            dt = current_time - last_updated
            return weight * exp(-self.decay * dt)

        min_key = min(self.data, key=effective_weight)
        del self.data[min_key]

    @override
    def get_data(self) -> List[BaseObservableUnit]:
        """
        Retrieve all observable units currently managed by the policy.
        Returns:
            List[BaseObservableUnit]: The list of managed units.
        """
        result = []
        for unit in self.data.keys():
            for case_id in self.data[unit][0]:
                u = unit.clone()
                u.set_case_id(case_id)
                result.append(u)
        return result

    @override
    def remove_elements(self, units: List[BaseObservableUnit]) -> None:
        """
        Remove the specified observable units from the policy.
        Args:
            units (List[BaseObservableUnit]): The units to remove.
        """
        for unit in units:
            if unit in self.data:
                case_ids, weight, updated = self.data[unit]
                case_ids.remove(unit.get_case_id())
                if len(case_ids) > 0:
                    self.data[unit] = (case_ids, weight, updated)
                else:
                    del self.data[unit]

    @override
    def get_mergeable_elements(self, case_id) -> List[BaseObservableUnit]:
        """
        Retrieve all mergeable observable units for a given case ID.
        Args:
            case_id: The case identifier to filter units.
        Returns:
            List[BaseObservableUnit]: The list of mergeable units for the case.
        """
        ret = []
        for unit in self.data.keys():
            if case_id in self.data[unit][0] and unit.is_mergeable():
                u = unit.clone()
                u.set_case_id(case_id)
                ret.append(u)
        return ret

