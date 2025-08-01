import math
from typing import List, override

from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit
from memory_manager.policies.base_policy import BasePolicy

class LossyCountPolicy(BasePolicy):
    """
    Memory management policy implementing the Lossy Counting algorithm.
    Maintains approximate frequency counts for observable units within a specified error bound (epsilon).
    """

    @override
    def __init__(self, epsilon: float) -> None:
        """
        Initialize the LossyCountPolicy.
        Args:
            epsilon (float): Error bound for frequency approximation (0 < epsilon < 1).
        """
        self.bucket_width = math.ceil(1 / epsilon)
        self.data = dict()  # {unit: [[unit, ...], delta]}
        self.N = 0  # Total number of processed units

    @override
    def update(self, unit: BaseObservableUnit) -> None:
        """
        Update the policy with a new observable unit.
        Adds the unit to the data structure and trims infrequent units at bucket boundaries.
        Args:
            unit (BaseObservableUnit): The unit to add or update.
        """
        self.N += 1
        if unit in self.data:
            self.data[unit][0].append(unit)
        else:
            self.data[unit] = [[unit], self._bucket_id() - 1]

        if self.N % self.bucket_width == 0:
            self.trim()

    @override
    def get_data(self) -> List[BaseObservableUnit]:
        """
        Retrieve all observable units currently managed by the policy.
        Returns:
            List[BaseObservableUnit]: The list of managed units.
        """
        units = []
        for entry in self.data.values():
            units.extend(entry[0])
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
                unit_list = self.data[unit][0]
                # Remove units matching both equality and case ID
                self.data[unit][0] = [u for u in unit_list if (u != unit and u.get_case_id() != unit.get_case_id())]
                if len(self.data[unit][0]) == 0:
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
        for entry in self.data.values():
            for unit in entry[0]:
                if unit.is_mergeable() and unit.get_case_id() == case_id:
                    ret.append(unit)
        return ret

    def _bucket_id(self):
        """
        Compute the current bucket ID based on the number of processed units.
        Returns:
            int: The current bucket ID.
        """
        return math.floor(self.N / self.bucket_width)

    def trim(self):
        """
        Remove units whose estimated frequency is too low to be significant.
        This is done at the end of each bucket.
        """
        bucket_id = self._bucket_id()
        items_to_remove = [item for item, (count, delta) in self.data.items() if len(count) + delta <= bucket_id]
        for item in items_to_remove:
            if item in self.data:
                del self.data[item]