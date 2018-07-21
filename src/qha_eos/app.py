from qha.cli.program import QHAProgram

from .patch import StaticHelmholtzFreeEnergyCalculator, StaticTemperatureVolumeCalculator
from .writer import FunctionOfPressureWriter, FunctionOfVolumeWriter


class QHAEOSProgram(QHAProgram):
    
    aliases = ['equation-of-state']

    def __init__(self):
        super().__init__()

    def init_parser(self, parser):
        super().init_parser(parser)
        parser.add_argument('--json', type=str)
        parser.add_argument('--txt', type=str)

    def run(self, namespace):
        if namespace.json:
            from .reader import JSONInputReader
            reader = JSONInputReader()
            data = reader.read(namespace.json)
        elif namespace.txt:
            from .reader import TabularInputReader
            reader = TabularInputReader()
            data = reader.read(namespace.txt)
        else:
            # TODO: print help
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
