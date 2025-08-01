from typing import List, override

from pybeamline.bevent import BEvent

from memory_manager.observable_unit_tools.handlers.base_observable_unit_handler import BaseObservableUnitHandler, U
from memory_manager.observable_unit_tools.units.trace_observable_unit import TraceObservableUnit


class TraceObservableUnitHandler(BaseObservableUnitHandler[TraceObservableUnit]):
    """
    Handler for TraceObservableUnit objects.
    Implements conversion between BEvent and TraceObservableUnit,
    merging units, and converting units back to events.
    """

    unit_class = TraceObservableUnit

    @override
    def __init__(self) -> None:
        """
        Initialize the TraceObservableUnitHandler.
        Calls the base class initializer.
        """
        super().__init__()

    @override
    def convert(self, event: BEvent) -> TraceObservableUnit:
        """
        Convert a BEvent to a TraceObservableUnit.
        Args:
            event (BEvent): The event to convert.
        Returns:
            TraceObservableUnit: The resulting observable unit.
        """
        return TraceObservableUnit([event])

    @override
    def merge(self, units: List[TraceObservableUnit]) -> List[TraceObservableUnit]:
        """
        Merge a list of TraceObservableUnit objects.
        If there are exactly two units, merge their event lists.
        Args:
            units (List[TraceObservableUnit]): The units to merge.
        Returns:
            List[TraceObservableUnit]: The merged unit as a single-element list, or empty list if not mergeable.
        """
        if len(units) == 2:
            ret = units[0]
            ret.events += units[1].events
            return [ret]
        return []

    @override
    def convert_back(self, units: List[TraceObservableUnit]) -> List[BEvent]:
        """
        Convert a list of TraceObservableUnit objects back to BEvent objects.
        Args:
            units (List[TraceObservableUnit]): The units to convert.
        Returns:
            List[BEvent]: The resulting list of events.
        """
        ret = []
        for unit in units:
            ret.extend(unit.events)
        return ret
