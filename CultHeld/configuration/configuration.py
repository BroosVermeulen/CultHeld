import os
from dataclasses import dataclass
from typing import Callable

from cultheld.configuration.utils.utils_configuration import AllInstances
import cultheld.venues.de_balie as de_balie
import cultheld.venues.studiok as studiok
import cultheld.venues.paradiso as paradiso


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

all_configuration_venues = AllInstances()
configuration_venues = all_configuration_venues.get_instances()

@dataclass
class ConfigurationVenues:
    ID: str
    venue: str
    type: str
    output_folder: str
    function: Callable
    add_to_combined_venues: bool = True
    append_to_config_instances: bool = True  # control from unit tests

    def __post_init__(self):
        """Add instance to the list of all instances
        """
        self.validate_input()

        if self.append_to_config_instances:
            all_configuration_venues.instances.append(self)

    def validate_input(self):
        """Validate if the input for the configuration is valid
        """
        assert isinstance(self.ID, str), f'ID is not an int, type is {type(self.ID)}.'


venue_001 = ConfigurationVenues(
    ID='venue_001',
    venue='de_balie',
    type='Actualiteit',
    output_folder=ROOT_DIR + '/../output/de_balie.csv',
    function=de_balie.main
)

venue_002 = ConfigurationVenues(
    ID='venue_002',
    venue='studiok',
    type='Bioscoop',
    output_folder=ROOT_DIR + '/../output/studiok.csv',
    function=studiok.main,
)

venue_003 = ConfigurationVenues(
    ID='venue_003',
    venue='paradiso',
    type='Concert',
    output_folder=ROOT_DIR + '/../output/paradiso.csv',
    function=paradiso.main,
)
