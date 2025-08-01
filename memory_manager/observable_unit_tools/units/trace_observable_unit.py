from typing import List, override

from pybeamline.bevent import BEvent

from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit
from memory_manager.tools.memory_mamager_helper import MemoryManagerHelper


class TraceObservableUnit(BaseObservableUnit):
    """
    Observable unit representing a sequence of BEvent objects that form the same trace.
    """

    @override
    def __init__(self, events: List[BEvent]) -> None:
        """
        Initialize the TraceObservableUnit with a list of BEvent objects.
        Args:
            events (List[BEvent]): The list of events in the trace.
        """
        super().__init__()
        self.events = events

    @override
    def get_case_id(self) -> str:
        """
        Return the case ID for this trace.
        Returns:
            str: The case ID, or "none" if the trace is empty.
        """
        if len(self.events) > 0:
            return self.events[0].get_trace_name()
        return "none"

    @override
    def is_mergeable(self) -> bool:
        """
        TraceObservableUnit objects are always mergeable, since a trace always can be extended with more events.
        Returns:
            bool: Always True.
        """
        return True

    @override
    def __eq__(self, other) -> bool:
        """
        Check equality with another TraceObservableUnit.
        Args:
            other: The object to compare with.
        Returns:
            bool: True if the case IDs are equal, False otherwise.
        """
        if not isinstance(other, TraceObservableUnit):
            return NotImplemented
        return self.get_case_id() == other.get_case_id()

    @override
    def __hash__(self):
        """
        Return the hash value of the TraceObservableUnit, based on the case ID.
        Returns:
            int: The hash value.
        """
        return hash(self.get_case_id())

    @override
    def set_case_id(self, case_id: str) -> None:
        new_events = []
        for event in self.events:
            new_events.append(MemoryManagerHelper.set_event_case_id(case_id, event))
        self.events = new_events

    @override
    def clone(self):
        new_events = []
        for event in self.events:
            new_events.append(MemoryManagerHelper.clone_event(event))
        return TraceObservableUnit(new_events)