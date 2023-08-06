from typing import Any, List


class AllInstances:
    """Capture all instances from configuration dataclass
    """
    instances: List[Any] = list()

    def __init__(self) -> None:
        self.instances = list()

    def get_instances(self) -> List[Any]:
        """Retrieve all instances
        """
        return self.instances
