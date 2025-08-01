from typing import override
from pybeamline.bevent import BEvent

from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit
from memory_manager.tools.memory_mamager_helper import MemoryManagerHelper


class EventObservableUnit(BaseObservableUnit):
    """
    Observable unit representing a single BEvent object.
    """

    @override
    def __init__(self, event: BEvent) -> None:
        """
        Initialize the EventObservableUnit with a BEvent.
        Args:
            event (BEvent): The event to wrap.
        """
        super().__init__()
        self.event = event

    @override
    def get_case_id(self) -> str:
        """
        Return the case ID for this event.
        Returns:
            str: The case ID.
        """
        return self.event.get_trace_name()

    @override
    def is_mergeable(self) -> bool:
        """
        EventObservableUnit objects are never mergeable, since they represent single events.
        Returns:
            bool: Always False.
        """
        return False

    @override
    def __eq__(self, other) -> bool:
        """
        Check equality with another EventObservableUnit.
        Args:
            other: The object to compare with.
        Returns:
            bool: True if the events are equal, False otherwise.
        """
        if not isinstance(other, EventObservableUnit):
            return NotImplemented
        return MemoryManagerHelper.events_equal(self.event, other.event)

    @override
    def clone(self):
        if self.event is None:
            return None
        return EventObservableUnit(MemoryManagerHelper.clone_event(self.event))

    @override
    def __hash__(self) -> int:
        """
        Return the hash value of the EventObservableUnit, based on the event.
        Returns:
            int: The hash value.
        """
        return MemoryManagerHelper.event_hash(self.event)

    @override
    def set_case_id(self, new_case_id: str) -> None:
        if self.event is not None:
            self.event = MemoryManagerHelper.set_event_case_id(new_case_id, self.event)