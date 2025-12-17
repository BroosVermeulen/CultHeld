from typing import Any


class AllInstances:
    """Capture all instances from configuration dataclass
    """
    instances: list[Any] = list()

    def __init__(self) -> None:
        self.instances = list()

    def get_instances(self) -> list[Any]:
        """Retrieve all instances
        """
        return self.instances
