import argparse

from qha.calculator.helmholtz_calculator.configuration import StructureConfiguration
from qha.calculator.helmholtz_calculator import SingleConfigurationHelmholtzFreeEnergyCalculator
from qha.calculator import TemperatureVolumeFieldCalculator
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

from qha.settings import DEFAULT_SETTING
from .thermo import static_thermodynamic_potentials
import copy

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

from qha.cli.results_writer import FieldResultsWriter
from qha.utils.units import QHAUnits

units = QHAUnits()

import numpy
import sys

class FunctionOfVolumeWriter(FieldResultsWriter):
    def __init__(self, calculator):
        self.calculator = calculator
    def write(self, prop_name, fp=sys.stdout, unit=None):
        fp.write('V / A^3\t%s / ??\n' % prop_name)
        fp.writelines([
            '%f\t%f\n' % tuple(row)
            for row in numpy.array([
                self.calculator.volume_array.to(units.angstrom ** 3).magnitude,
                self.get_prop(prop_name, unit)[0]
            ]).transpose().tolist()
        ])

class FunctionOfPressureWriter(FieldResultsWriter):
    def __init__(self, calculator):
        self.calculator = calculator.temperature_pressure_field_adapter
    def write(self, prop_name, fp=sys.stdout, unit=None):
        fp.write('P / GPa\t%s / ??\n' % prop_name)
        fp.writelines([
            '%f\t%f\n' % tuple(row)
            for row in numpy.array([
                self.calculator.pressure_array.to(units.GPa).magnitude,
                self.get_prop(prop_name, unit)[0]
            ]).transpose().tolist()
        ])

def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--json', type=str)
    argument_parser.add_argument('--txt', type=str)
    namespace = argument_parser.parse_args()

    if namespace.json:
        from .reader import JSONInputReader
        reader = JSONInputReader()
        data = reader.read(namespace.json)
    elif namespace.txt:
        from .reader import TabularInputReader
        reader = TabularInputReader()
        data = reader.read(namespace.txt)
    else:
        argument_parser.print_help()
        exit()
    
    calculator = StaticTemperatureVolumeCalculator(data)
    calculator.calculate()

    fv_writer = FunctionOfVolumeWriter(calculator)
    fp_writer = FunctionOfPressureWriter(calculator)

    fv_writer.write('F')
    fv_writer.write('G')
    fv_writer.write('H')
    fv_writer.write('U')

    fp_writer.write('F')
    fp_writer.write('G')
    fp_writer.write('H')
    fp_writer.write('U')

    fp_writer.write('Bt')
    fp_writer.write('Btp')
