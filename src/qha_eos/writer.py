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
