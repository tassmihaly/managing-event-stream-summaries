from typing import List, Callable

from pybeamline.bevent import BEvent


class MemoryManagerHelper:
    """
    Helper class providing static utility methods for event comparison and set operations.
    """

    @staticmethod
    def events_equal(event1: BEvent, event2: BEvent) -> bool:
        """
        Check if two BEvent objects are equal based on event name, trace name, and process name.
        Args:
            event1 (BEvent): The first event.
            event2 (BEvent): The second event.
        Returns:
            bool: True if both events are equal or both None, False otherwise.
        """
        if event1 is None or event2 is None:
            return event1 == event2
        return (event1.get_event_name() == event2.get_event_name() and
                event1.get_trace_name() == event2.get_trace_name() and
                event1.get_process_name() == event2.get_process_name())

    @staticmethod
    def event_names_equal(event1: BEvent, event2: BEvent) -> bool:
        """
        Check if two BEvent objects have the same event name.
        Args:
            event1 (BEvent): The first event.
            event2 (BEvent): The second event.
        Returns:
            bool: True if event names are equal, False otherwise.
        """
        event_name1 = event1.get_event_name() if event1 is not None else None
        event_name2 = event2.get_event_name() if event2 is not None else None
        return event_name1 == event_name2

    @staticmethod
    def event_hash(event: BEvent) -> int:
        """
        Compute a hash value for a BEvent based on event name, trace name, and event time.
        Args:
            event (BEvent): The event to hash.
        Returns:
            int: The hash value, or 0 if event is None.
        """
        if event is None:
            return 0
        return hash((
            event.get_event_name(),
            event.get_trace_name(),
            event.get_event_time()
        ))

    @staticmethod
    def intersect_with_custom_eq(list1: List[BEvent], list2: List[BEvent], eq_func: Callable[[BEvent, BEvent], bool]) -> List[BEvent]:
        """
        Return the intersection of two lists using a custom equality function.
        Args:
            list1 (List[BEvent]): The first list.
            list2 (List[BEvent]): The second list.
            eq_func (Callable): Function to compare two BEvent objects.
        Returns:
            List[BEvent]: List of elements present in both lists according to eq_func.
        """
        return [x for x in list1 if any(eq_func(x, y) for y in list2)]

    @staticmethod
    def difference_with_custom_eq(list1: List[BEvent], list2: List[BEvent], eq_func: Callable[[BEvent, BEvent], bool]) -> List[BEvent]:
        """
        Return the difference of two lists using a custom equality function.
        Args:
            list1 (List[BEvent]): The first list.
            list2 (List[BEvent]): The second list.
            eq_func (Callable): Function to compare two BEvent objects.
        Returns:
            List[BEvent]: List of elements in list1 not present in list2 according to eq_func.
        """
        return [x for x in list1 if not any(eq_func(x, y) for y in list2)]

    @staticmethod
    def set_event_case_id(case_id, event: BEvent):
        """
        Create a copy of the given BEvent with a new case (trace) ID.

        Args:
            case_id: The new case ID (used as the trace name).
            event (BEvent): The original event to modify.

        Returns:
            BEvent: A new BEvent instance with the updated case ID,
                    or None if the input event is None.
        """
        if event is not None:
            return BEvent(event.get_event_name(), case_id, event.get_process_name(), event.get_event_time())

    @staticmethod
    def clone_event(event: BEvent) -> BEvent:
        """
        Create an exact copy of a given BEvent.

        Args:
            event (BEvent): The event to clone.

        Returns:
            BEvent: A new BEvent instance with the same properties as the original,
                    or None if the input event is None.
        """
        if event is not None:
            return BEvent(event.get_event_name(), event.get_trace_name(), event.get_process_name(), event.get_event_time())


