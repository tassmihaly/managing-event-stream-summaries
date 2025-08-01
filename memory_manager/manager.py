from typing import List

from pybeamline.bevent import BEvent

from memory_manager.observable_unit_tools.handlers.base_observable_unit_handler import BaseObservableUnitHandler
from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit
from memory_manager.policies.base_policy import BasePolicy


class MemoryManager:
    """
    Main class for managing memory using a specified policy and handler.
    Handles the addition of events, merging of observable units, and retrieval of managed data.
    """

    def __init__(self, policy: BasePolicy, handler: BaseObservableUnitHandler):
        """
        Initialize the MemoryManager with a policy and handler.
        Args:
            policy (BasePolicy): The memory management policy to use.
            handler (BaseObservableUnitHandler): The handler for observable units.
        Raises:
            TypeError: If handler.unit_class is not a subclass of BaseObservableUnit.
        """
        self.policy = policy
        self.handler = handler
        if not issubclass(handler.unit_class, BaseObservableUnit):
            raise TypeError(f"Handler's unit_class {handler.unit_class} must be a subclass of BaseObservableUnit.")

    def add_event(self, event: BEvent) -> None:
        """
        Add a new event to the memory manager.
        Converts the event to an observable unit, merges if possible, and updates the policy.
        Args:
            event (BEvent): The event to add.
        """
        observable_unit: BaseObservableUnit = self.handler.convert(event)
        mergeable_units: List[BaseObservableUnit] = self.policy.get_mergeable_elements(observable_unit.get_case_id())
        if len(mergeable_units) > 0:
            self.policy.remove_elements(mergeable_units)
            mergeable_units.append(observable_unit)
            merged_observable_units = self.handler.merge(mergeable_units)
            for merged_observable_unit in merged_observable_units:
                self.policy.update(merged_observable_unit)
        else:
            self.policy.update(observable_unit)

    def get_data(self) -> List[BEvent]:
        """
        Retrieve all managed events as a list of BEvent objects.
        Returns:
            List[BEvent]: The list of managed events.
        """
        return self.handler.convert_back(self.policy.get_data())
















