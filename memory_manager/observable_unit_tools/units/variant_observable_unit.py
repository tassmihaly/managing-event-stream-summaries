from typing import List, override

from pybeamline.bevent import BEvent

from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit
from memory_manager.tools.memory_mamager_helper import MemoryManagerHelper


class VariantObservableUnit(BaseObservableUnit):
    """
    Observable unit representing a variant, i.e., a sequence of activities.
    """

    @override
    def __init__(self, events: List[BEvent]) -> None:
        """
        Initialize the VariantObservableUnit with a list of BEvent objects.
        Args:
            events (List[BEvent]): The list of events in the variant.
        """
        super().__init__()
        self.events: List[BEvent] = events

    @override
    def get_case_id(self) -> str:
        """
        Return the case ID for this variant.
        Returns:
            str: The case ID, or "none" if the variant is empty.
        """
        if len(self.events) > 0:
            return self.events[0].get_trace_name()
        return "none"

    @override
    def is_mergeable(self) -> bool:
        """
        VariantObservableUnit objects are always mergeable, since a variant can always be extended with more activities.
        Returns:
            bool: Always True.
        """
        return True

    @override
    def __eq__(self, other) -> bool:
        """
        Check equality with another VariantObservableUnit.
        Args:
            other: The object to compare with.
        Returns:
            bool: True if the event sequences are equal, False otherwise.
        """
        if not isinstance(other, VariantObservableUnit):
            return NotImplemented
        for i in range(0, min(len(self.events), len(other.events))):
            if not MemoryManagerHelper.event_names_equal(self.events[i], other.events[i]):
                return False
        return len(self.events) == len(other.events)

    @override
    def set_case_id(self, case_id: str) -> None:
        new_events = []
        for event in self.events:
            new_events.append(MemoryManagerHelper.set_event_case_id(case_id, event))
        self.events = new_events

    @override
    def __hash__(self) -> int:
        """
        Return the hash value of the VariantObservableUnit, based on the event names.
        Returns:
            int: The hash value.
        """
        return hash(tuple(
            e.get_event_name() for e in self.events
        ))

    @override
    def clone(self):
        new_events = []
        for event in self.events:
            new_events.append(MemoryManagerHelper.clone_event(event))
        return VariantObservableUnit(new_events)


