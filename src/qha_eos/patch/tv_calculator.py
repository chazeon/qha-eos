import copy
import numpy

from qha.settings import DEFAULT_SETTING
from .thermo import static_thermodynamic_potentials
from qha.calculator import TemperatureVolumeFieldCalculator
from .helmholtz import StaticHelmholtzFreeEnergyCalculator


class StaticTemperatureVolumeCalculator(TemperatureVolumeFieldCalculator):
    def __init__(self, pve_data):
        settings = copy.deepcopy(DEFAULT_SETTING)
        settings['static_only'] = True
        self._pve_data = pve_data
        settings['P_MIN'] = numpy.min(pve_data[:]['pressure'])
        settings['NTV'] = numpy.ptp(pve_data[:]['pressure']) / settings['DELTA_P']
        super().__init__(settings)
    def calculate_thermodynamic_potentials(self):
        self._thermodynamic_potentials = \
            static_thermodynamic_potentials(
                self.volume_array.magnitude,
                self.helmholtz_free_energies.magnitude,
                self.pressures.magnitude
            )

    def make_helmholtz_free_energy_calculator(self):
        self._helmholtz_free_energy_calculator = StaticHelmholtzFreeEnergyCalculator(self.settings, self._pve_data)
