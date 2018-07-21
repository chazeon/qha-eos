from qha.calculator.helmholtz_calculator.configuration import StructureConfiguration
from qha.calculator.helmholtz_calculator import SingleConfigurationHelmholtzFreeEnergyCalculator

from lazy_property import LazyProperty
from qha.utils.units import QHAUnits


units = QHAUnits()

class StaticHelmholtzFreeEnergyCalculator(SingleConfigurationHelmholtzFreeEnergyCalculator):
    def __init__(self, settings, data):
        super().__init__(settings)
        self.configuration = StructureConfiguration(
            formula_unit_number=1,
            volumes=data[:]['volume'],
            static_energies=data[:]['energy'],
            frequencies=[[] for i in range(len(data))],
            q_weights=[],
        )

    @LazyProperty
    @units.wraps(units.kelvin, None)
    def temperature_array(self):
        return [0.0]

    def read_input(self):
        pass
