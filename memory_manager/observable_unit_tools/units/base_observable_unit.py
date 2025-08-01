from abc import ABC, abstractmethod

class BaseObservableUnit(ABC):
    """
    Abstract base class for observable units.
    Defines the required interface for all observable unit types.
    """

    @abstractmethod
    def __init__(self) -> None:
        """
        Initialize the observable unit.
        Subclasses should implement any required initialization logic.
        """
        pass

    @abstractmethod
    def get_case_id(self) -> str:
        """
        Return a unique identifier for the case associated with this unit.
        Returns:
            str: The case identifier.
        """
        pass

    @abstractmethod
    def is_mergeable(self) -> bool:
        """
        Determine if this unit can be merged with another unit.
        Returns:
            bool: True if mergeable, False otherwise.
        """
        pass

    @abstractmethod
    def set_case_id(self, case_id: str) -> None:
        pass

    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        """
        Check equality with another observable unit.
        Args:
            other: The object to compare with.
        Returns:
            bool: True if equal, False otherwise.
        """
        pass

    @abstractmethod
    def __hash__(self):
        """
        Return the hash value of the observable unit.
        Returns:
            int: The hash value.
        """
        pass

