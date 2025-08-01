from typing import List

from typing import override
from pybeamline.bevent import BEvent

from memory_manager.observable_unit_tools.handlers.base_observable_unit_handler import BaseObservableUnitHandler, U
from memory_manager.observable_unit_tools.units.dfr_observable_unit import DfrObservableUnit


class DfrObservableUnitHandler(BaseObservableUnitHandler[DfrObservableUnit]):
    """
    Handler for DfrObservableUnit objects.
    Implements conversion between BEvent and DfrObservableUnit,
    merging units, and converting units back to events.
    """

    unit_class = DfrObservableUnit

    @override
    def __init__(self) -> None:
        """
        Initialize the DfrObservableUnitHandler.
        Calls the base class initializer.
        """
        super().__init__()

    @override
    def convert(self, event: BEvent) -> DfrObservableUnit:
        """
        Convert a BEvent to a DfrObservableUnit.
        Args:
            event (BEvent): The event to convert.
        Returns:
            DfrObservableUnit: The resulting observable unit.
        """
        return DfrObservableUnit(event, None)

    @override
    def merge(self, units: List[DfrObservableUnit]) -> List[DfrObservableUnit]:
        """
        Merge a list of DfrObservableUnit objects.
        If there are exactly two units, merge their 'first' attributes.
        Args:
            units (List[DfrObservableUnit]): The units to merge.
        Returns:
            List[DfrObservableUnit]: The merged units, or an empty list if not mergeable.
        """
        if len(units) == 2:
            return [DfrObservableUnit(units[0].first, units[1].first), units[1]]
        return []

    @override
    def convert_back(self, units: List[DfrObservableUnit]) -> List[BEvent]:
        """
        Convert a list of DfrObservableUnit objects back to BEvent objects.
        Ensures no duplicates in the returned list.
        Args:
            units (List[DfrObservableUnit]): The units to convert.
        Returns:
            List[BEvent]: The resulting list of events.
        """
        ret = []
        for unit in units:
            if unit.first is not None:
                if unit.first not in ret:
                    ret.append(unit.first)
            if unit.second is not None:
                if unit.second not in ret:
                    ret.append(unit.second)
        return ret
