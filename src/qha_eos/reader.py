import json
import numpy

class InputReader:
    _INPUT_DTYPE = {
        'names': ('pressure', 'volume', 'energy'),
        'formats': ('f4', 'f4', 'f4')
    }
    def read(self, fname: str) -> numpy.ndarray:
        raise NotImplementedError()



class TabularInputReader(InputReader):
    def read(self, fname: str) -> numpy.ndarray:
        data = numpy.loadtxt(fname, dtype=super()._INPUT_DTYPE)
        return data

class JSONInputReader(InputReader):
    def __init__(self, getter: callable = lambda item: item):
        self._getter = getter

    def read(self, fname: str) -> numpy.ndarray:
        with open(fname, encoding='utf8') as fp:
            data = json.load(fp)
        return numpy.array(list(zip(
            self._getter(data)['pressure'],
            self._getter(data)['volume'],
            self._getter(data)['energy']
        )), dtype=super()._INPUT_DTYPE)