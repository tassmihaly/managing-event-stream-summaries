from typing import List, override

from pybeamline.bevent import BEvent

from memory_manager.observable_unit_tools.handlers.base_observable_unit_handler import BaseObservableUnitHandler, U
from memory_manager.observable_unit_tools.units.event_observable_unit import EventObservableUnit


class EventObservableUnitHandler(BaseObservableUnitHandler[EventObservableUnit]):
    """
    Handler for EventObservableUnit objects.
    Implements conversion between BEvent and EventObservableUnit,
    merging units, and converting units back to events.
    """

    unit_class = EventObservableUnit

    @override
    def __init__(self) -> None:
        """
        Initialize the EventObservableUnitHandler.
        Calls the base class initializer.
        """
        super().__init__()

    @override
    def merge(self, units: List[EventObservableUnit]) -> List[EventObservableUnit]:
        """
        Merge a list of EventObservableUnit objects.
        For this handler, merging is not supported, since events can not be merged. Returns an empty list.
        Args:
            units (List[EventObservableUnit]): The units to merge.
        Returns:
            List[EventObservableUnit]: Always an empty list.
        """
        return []

    @override
    def convert(self, event: BEvent) -> U:
        """
        Convert a BEvent to an EventObservableUnit.
        Args:
            event (BEvent): The event to convert.
        Returns:
            EventObservableUnit: The resulting observable unit.
        """
        return EventObservableUnit(event)

    @override
    def convert_back(self, units: List[EventObservableUnit]) -> List[BEvent]:
        """
        Convert a list of EventObservableUnit objects back to BEvent objects.
        Args:
            units (List[EventObservableUnit]): The units to convert.
        Returns:
            List[BEvent]: The resulting list of events.
        """
        return [unit.event for unit in units]
