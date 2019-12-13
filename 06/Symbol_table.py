import sys


class Symbol_table:
    def __init__(self):
        # predefined symbols.
        self._table = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576,
        }
        # R0 - R15
        for i in range(16):
            self._table[f'R{i}'] = i
        # add_entry starts from 16
        self._i = 16

    def add_entry(self, symbol: str, address: int = None):
        if address is None:
            # automatic memory allocation for new var.
            address = self._i
            self._i += 1
        self._table[symbol] = address

    def contains(self, symbol: str) -> bool:
        r = self._table.get(symbol, None)
        if r is None:
            return False
        else:
            return True

    def get_address(self, symbol: str) -> int:
        return self._table.get(symbol)


sys.modules[__name__] = Symbol_table
