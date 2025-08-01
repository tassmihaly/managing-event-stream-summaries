from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, List

from pybeamline.bevent import BEvent
from memory_manager.observable_unit_tools.units.base_observable_unit import BaseObservableUnit

U = TypeVar("U", bound=BaseObservableUnit)

class BaseObservableUnitHandler(ABC, Generic[U]):
    """
    Abstract base class for handlers that process observable units.
    Subclasses should implement methods for converting events to units,
    merging units, and converting units back to events.
    """
    unit_class: Type[U]  # The class of observable unit this handler manages

    @abstractmethod
    def __init__(self) -> None:
        """
        Initialize the handler.
        Subclasses may set up additional state or configuration here.
        """
        pass

    @abstractmethod
    def convert(self, event: BEvent) -> U:
        """
        Convert a BEvent to an observable unit.
        Args:
            event (BEvent): The event to convert.
        Returns:
            U: The resulting observable unit.
        """
        pass

    @abstractmethod
    def merge(self, units: List[U]) -> List[U]:
        """
        Merge a list of observable units.
        Args:
            units (List[U]): The units to merge.
        Returns:
            List[U]: The merged units.
        """
        pass

    @abstractmethod
    def convert_back(self, units: List[U]) -> List[BEvent]:
        """
        Convert a list of observable units back to BEvents.
        Args:
            units (List[U]): The units to convert.
        Returns:
            List[BEvent]: The resulting events.
        """
        pass

