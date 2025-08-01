from typing import List, override, Dict

from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit
from memory_manager.policies.base_policy import BasePolicy


class LossyCountWithBudgetPolicy(BasePolicy):
    """
    Memory management policy that combines lossy counting with a fixed budget.
    Maintains a limited number of observable units, trimming based on frequency and recency.
    """

    @override
    def __init__(self, budget: int) -> None:
        """
        Initialize the LossyCountWithBudgetPolicy.
        Args:
            budget (int): Maximum number of unique keys to keep.
        """
        self.budget: int = budget
        self.data: Dict[BaseObservableUnit, tuple[list[str], int]] = {}
        self.N: int = 0

    @override
    def update(self, unit: BaseObservableUnit) -> None:
        """
        Update the policy with a new observable unit.
        Adds or updates the unit and trims if over budget.
        Args:
            unit (BaseObservableUnit): The unit to add or update.
        """
        self.N += 1
        if unit in self.data:
            lst = self.data[unit][0]
            lst.append(unit.get_case_id())
            lst = lst[-self.budget:]
            self.data[unit] = (lst, self.N)
        else:
            self.data[unit] = ([unit.get_case_id()], self.N)

        if len(self.data) > self.budget:
            self.trim()

    def trim(self) -> None:
        """
        Remove the least valuable entry to maintain the budget.
        Uses a weighted score of frequency and recency.
        """
        alpha = 0.6
        min_lifetime = (self.budget // 3) * 2

        # Filter out entries that are too new to be trimmed
        candidates = {
            k: v for k, v in self.data.items()
            if (self.N - v[1]) > min_lifetime
        }

        # If no candidates to trim, fall back to oldest anyway
        if not candidates:
            candidates = self.data

        min_key = min(
            candidates,
            key=lambda k: len(self.data[k][0]) * alpha + (self.N - self.data[k][1]) * (1 - alpha)
        )
        del self.data[min_key]

    @override
    def get_data(self) -> List[BaseObservableUnit]:
        """
        Retrieve all observable units currently managed by the policy.
        Returns:
            List[BaseObservableUnit]: The list of managed units.
        """
        units = []
        for unit in self.data.keys():
            for case_id in self.data[unit][0]:
                u = unit.clone()
                u.set_case_id(case_id)
                units.append(u)
        return units

    @override
    def remove_elements(self, units: List[BaseObservableUnit]) -> None:
        """
        Remove the specified observable units from the policy.
        Args:
            units (List[BaseObservableUnit]): The units to remove.
        """
        for unit in units:
            if unit in self.data:
                lst, n = self.data[unit]
                lst.remove(unit.get_case_id())
                if len(lst) == 0:
                    del self.data[unit]
                else:
                    self.data[unit] = (lst, n)

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
            if unit.is_mergeable() and case_id in self.data[unit][0]:
                u = unit.clone()
                u.set_case_id(case_id)
                ret.append(u)
        return ret