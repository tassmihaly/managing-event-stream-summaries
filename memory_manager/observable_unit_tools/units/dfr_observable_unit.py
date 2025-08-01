from typing import Optional
from typing import override
from pybeamline.bevent import BEvent

from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit
from memory_manager.tools.memory_mamager_helper import MemoryManagerHelper


class DfrObservableUnit(BaseObservableUnit):
    """
    Observable unit representing a Directly-Follows Relation (DFR) between two BEvent objects.
    """

    def __init__(self, first: Optional[BEvent], second: Optional[BEvent]) -> None:
        """
        Initialize the DfrObservableUnit with two optional BEvent objects.
        Args:
            first (Optional[BEvent]): The first event in the pair.
            second (Optional[BEvent]): The second event in the pair.
        """
        self.first = first
        self.second = second

    @override
    def get_case_id(self) -> str | None:
        """
        Return the case ID of the DFR observable unit.
        Returns:
            str | None: The case ID, or None if the DFR is empty.
        """
        if self.first is not None:
            return self.first.get_trace_name()
        if self.second is not None:
            return self.second.get_trace_name()
        return None

    @override
    def is_mergeable(self) -> bool:
        """
        Determine if this unit can be merged with another.
        Returns:
            bool: True if either event is None, False otherwise.
        """
        return self.first is None or self.second is None

    @override
    def __eq__(self, other) -> bool:
        """
        Check equality with another DfrObservableUnit.
        Args:
            other: The object to compare with.
        Returns:
            bool: True if both events are equal, False otherwise.
        """
        if not isinstance(other, DfrObservableUnit):
            return NotImplemented
        return (
            MemoryManagerHelper.event_names_equal(self.first, other.first) and
            MemoryManagerHelper.event_names_equal(self.second, other.second)
        )

    @override
    def clone(self):
        first = None
        second = None
        if self.first is not None:
            first = MemoryManagerHelper.clone_event(self.first)
        if self.second is not None:
            second = MemoryManagerHelper.clone_event(self.second)
        return DfrObservableUnit(first, second)

    @override
    def __hash__(self):
        """
        Return the hash value of the DfrObservableUnit, based on event names.
        Returns:
            int: The hash value.
        """
        first_name = self.first.get_event_name() if self.first is not None else None
        second_name = self.second.get_event_name() if self.second is not None else None
        return hash((first_name, second_name))

    @override
    def set_case_id(self, case_id: str) -> None:
        if self.first is not None:
            self.first = MemoryManagerHelper.set_event_case_id(case_id, self.first)
        if self.second is not None:
            self.second = MemoryManagerHelper.set_event_case_id(case_id, self.second)