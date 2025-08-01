from typing import List

from typing_extensions import override

from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit
from memory_manager.policies.base_policy import BasePolicy


class SlidingWindowPolicy(BasePolicy):
    """
    Memory management policy implementing a sliding window.
    Maintains only the most recent observable units up to a fixed window size.
    """

    @override
    def __init__(self, window_size: int) -> None:
        """
        Initialize the SlidingWindowPolicy.
        Args:
            window_size (int): The maximum number of units to keep in the window.
        """
        super().__init__()
        self.window_size = window_size
        self.data: List[BaseObservableUnit] = []

    @override
    def get_data(self) -> List[BaseObservableUnit]:
        """
        Retrieve all observable units currently managed by the policy.
        Returns:
            List[BaseObservableUnit]: The list of managed units.
        """
        return self.data

    @override
    def update(self, unit: BaseObservableUnit) -> None:
        """
        Update the policy with a new observable unit.
        Adds the unit and ensures the window does not exceed its size.
        Args:
            unit (BaseObservableUnit): The unit to add.
        """
        self.data.append(unit)
        self.data = self.data[-self.window_size:]

    @override
    def remove_elements(self, units: List[BaseObservableUnit]) -> None:
        """
        Remove the specified observable units from the policy.
        Args:
            units (List[BaseObservableUnit]): The units to remove.
        """
        self.data[:] = [
            u for u in self.data
            if all(
                not (u == rem and u.get_case_id() == rem.get_case_id())
                for rem in units
            )
        ]

    @override
    def get_mergeable_elements(self, case_id: str) -> List[BaseObservableUnit]:
        """
        Retrieve all mergeable observable units for a given case ID.
        Args:
            case_id (str): The case identifier to filter units.
        Returns:
            List[BaseObservableUnit]: The list of mergeable units for the case.
        """
        return [x for x in self.data if x.is_mergeable() and x.get_case_id() == case_id]
