from typing import List, override
import random

from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit
from memory_manager.policies.base_policy import BasePolicy


class ReservoirSamplingPolicy(BasePolicy):
    """
    Memory management policy implementing reservoir sampling.
    Maintains a random sample of observable units up to a fixed budget.
    """

    @override
    def __init__(self, budget: int) -> None:
        """
        Initialize the ReservoirSamplingPolicy.
        Args:
            budget (int): Maximum number of units to keep in the reservoir.
        """
        self.budget: int = budget
        self.data: List[BaseObservableUnit] = []
        self.N: int = 0  # Total elements seen

    @override
    def update(self, unit: BaseObservableUnit) -> None:
        """
        Update the policy with a new observable unit.
        Adds the unit to the reservoir or replaces an existing one at random if over budget.
        Args:
            unit (BaseObservableUnit): The unit to add or update.
        """
        self.N += 1
        if len(self.data) < self.budget:
            self.data.append(unit)
        else:
            replace_idx = random.randint(0, self.N - 1)
            if replace_idx < self.budget:
                self.data[replace_idx] = unit

    @override
    def get_data(self) -> List[BaseObservableUnit]:
        """
        Retrieve all observable units currently managed by the policy.
        Returns:
            List[BaseObservableUnit]: The list of managed units.
        """
        return self.data

    @override
    def remove_elements(self, units: List[BaseObservableUnit]) -> None:
        """
        Remove the specified observable units from the policy.
        Args:
            units (List[BaseObservableUnit]): The units to remove.
        """
        to_remove = set((u.get_case_id(), u) for u in units)
        self.data = [u for u in self.data if (u.get_case_id(), u) not in to_remove]

    @override
    def get_mergeable_elements(self, case_id) -> List[BaseObservableUnit]:
        """
        Retrieve all mergeable observable units for a given case ID.
        Args:
            case_id: The case identifier to filter units.
        Returns:
            List[BaseObservableUnit]: The list of mergeable units for the case.
        """
        return [u for u in self.data if u.get_case_id() == case_id and u.is_mergeable()]
