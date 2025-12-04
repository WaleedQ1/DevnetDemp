from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Set
import logging

"""
Basic feature implementation for feature toggles and simple transformations.

Save as: /C:/Users/razan/devnet/DevnetDemp/Feature/feature.py
"""


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dataclass
class Feature:
    """
    A simple feature toggle with an optional transformation function.

    - name: feature identifier
    - enabled: whether the feature is active
    - dependencies: other feature names required for this feature to be available
    - transformer: optional callable applied to data when the feature is active
    """
    name: str
    enabled: bool = False
    dependencies: List[str] = field(default_factory=list)
    transformer: Optional[Callable[[Any], Any]] = None
    description: str = ""

    def enable(self) -> None:
        self.enabled = True
        logger.info("Feature '%s' enabled", self.name)

    def disable(self) -> None:
        self.enabled = False
        logger.info("Feature '%s' disabled", self.name)

    def is_available(self, active_features: Set[str]) -> bool:
        """
        Check if this feature is available given a set of active feature names.
        """
        missing = set(self.dependencies) - active_features
        if missing:
            logger.debug("Feature '%s' missing dependencies: %s", self.name, missing)
            return False
        return True

    def apply(self, data: Any, active_features: Optional[Set[str]] = None) -> Any:
        """
        Apply the feature's transformer to data if enabled and dependencies are satisfied.
        If no transformer is set or the feature is inactive / unavailable, returns data unchanged.
        """
        if not self.enabled:
            logger.debug("Feature '%s' is disabled; returning data unchanged", self.name)
            return data

        if active_features is None:
            active_features = set()

        if not self.is_available(active_features):
            logger.debug("Feature '%s' is unavailable due to dependencies; returning data unchanged", self.name)
            return data

        if self.transformer is None:
            logger.debug("Feature '%s' has no transformer; returning data unchanged", self.name)
            return data

        try:
            result = self.transformer(data)
            logger.info("Feature '%s' applied successfully", self.name)
            return result
        except Exception:
            logger.exception("Feature '%s' transformer raised an exception; returning original data", self.name)
            return data


# Example usage
if __name__ == "__main__":
    # A simple transformer that uppercases strings
    def to_upper(s: Any) -> Any:
        if isinstance(s, str):
            return s.upper()
        return s

    upper_feature = Feature(name="uppercase", description="Uppercase string inputs", transformer=to_upper)
    print("Input:", "hello world")
    print("Output (disabled):", upper_feature.apply("hello world"))

    upper_feature.enable()
    # no dependencies
    print("Output (enabled):", upper_feature.apply("hello world"))

    # Example with dependencies
    dependent = Feature(name="dependent", dependencies=["uppercase"], transformer=lambda s: f"[{s}]")
    dependent.enable()
    # since 'uppercase' is enabled, include it in active_features
    print("Dependent output (with uppercase active):", dependent.apply("data", active_features={"uppercase"}))
    # if dependency not active, data is unchanged
    print("Dependent output (without dependencies):", dependent.apply("data", active_features=set()))
    print('Welcome to myscript.py! as we are learning DevAsc course')