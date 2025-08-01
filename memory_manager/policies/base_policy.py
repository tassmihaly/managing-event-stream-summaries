from abc import ABC, abstractmethod
from typing import List

from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit


class BasePolicy(ABC):
    """
    Abstract base class for memory management policies.
    Defines the required interface for all policy types.
    """

    @abstractmethod
    def __init__(self) -> None:
        """
        Initialize the policy.
        Subclasses should implement any required initialization logic.
        """
        pass

    @abstractmethod
    def update(self, unit: BaseObservableUnit) -> None:
        """
        Update the policy with a new observable unit.
        Args:
            unit (BaseObservableUnit): The unit to add or update in the policy.
        """
        pass

    @abstractmethod
    def get_data(self) -> List[BaseObservableUnit]:
        """
        Retrieve all observable units currently managed by the policy.
        Returns:
            List[BaseObservableUnit]: The list of managed units.
        """
        pass

    @abstractmethod
    def remove_elements(self, units: List[BaseObservableUnit]) -> None:
        """
        Remove the specified observable units from the policy.
        Args:
            units (List[BaseObservableUnit]): The units to remove.
        """
        pass

    @abstractmethod
    def get_mergeable_elements(self, case_id) -> List[BaseObservableUnit]:
        """
        Retrieve all mergeable observable units for a given case ID.
        Args:
            case_id: The case identifier to filter units.
        Returns:
            List[BaseObservableUnit]: The list of mergeable units for the case.
        """
        pass
