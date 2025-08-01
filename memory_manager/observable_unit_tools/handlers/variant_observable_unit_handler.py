from typing import List, override

from pybeamline.bevent import BEvent

from memory_manager.observable_unit_tools.handlers.base_observable_unit_handler import BaseObservableUnitHandler, U
from memory_manager.observable_unit_tools.units.variant_observable_unit import VariantObservableUnit


class VariantObservableUnitHandler(BaseObservableUnitHandler[VariantObservableUnit]):
    """
    Handler for VariantObservableUnit objects.
    Implements conversion between BEvent and VariantObservableUnit,
    merging units, and converting units back to events.
    """

    unit_class = VariantObservableUnit

    @override
    def __init__(self) -> None:
        """
        Initialize the VariantObservableUnitHandler.
        Calls the base class initializer.
        """
        super().__init__()

    @override
    def convert(self, event: BEvent) -> VariantObservableUnit:
        """
        Convert a BEvent to a VariantObservableUnit.
        Args:
            event (BEvent): The event to convert.
        Returns:
            VariantObservableUnit: The resulting observable unit.
        """
        return VariantObservableUnit([event])

    @override
    def merge(self, units: List[VariantObservableUnit]) -> List[VariantObservableUnit]:
        """
        Merge a list of VariantObservableUnit objects.
        If there are exactly two units, merge their event lists.
        Args:
            units (List[VariantObservableUnit]): The units to merge.
        Returns:
            List[VariantObservableUnit]: The merged unit as a single-element list, or empty list if not mergeable.
        """
        if len(units) == 2:
            ret = units[0]
            ret.events += units[1].events
            return [ret]
        return []

    @override
    def convert_back(self, units: List[VariantObservableUnit]) -> List[BEvent]:
        """
        Convert a list of VariantObservableUnit objects back to BEvent objects.
        Args:
            units (List[VariantObservableUnit]): The units to convert.
        Returns:
            List[BEvent]: The resulting list of events.
        """
        ret = []
        for unit in units:
            ret.extend(unit.events)
        return ret