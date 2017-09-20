from .numeric import Numeric

class SHAUNPP(object):
    def __init__(self, shaun, indent_symbol='  '):
        self.shaun = shaun
        self.indent_symbol = indent_symbol
        self.indent_list = []
        self.fs = ''

    def print(self, to_print):
        lst = [ (lambda x: isinstance(x, (list, tuple)), self.print_list)
              , (lambda x: isinstance(x, dict), self.print_object)
              , (lambda x: isinstance(x, bool), self.print_bool)
              , (lambda x: isinstance(x, (int, float, Numeric)), self.print_numeric)
              , (lambda x: x is None, self.print_null)
              , (lambda x: isinstance(x, str), self.print_string) ]

        for (cond, f) in lst:
            if cond(to_print):
                return f(to_print)

    def indent(self):
        self.put(''.join(self.indent_list))

    def inc(self, sym=None):
        if sym is None:
            sym = self.indent_symbol
        else:
            sym = sym * ' '
        self.indent_list.append(sym)

    def dec(self):
        del self.indent_list[len(self.indent_list)-1]

    def put(self, string):
        self.fs = self.fs + string

    def print_list(self, lst):
        self.put('[')
        self.inc(2)
        for e in lst:
            self.put('\n')
            self.indent()
            self.print(e)
        self.dec()
        self.put('\n')
        self.indent()
        self.put(']')

    def print_object(self, obj):
        self.put('{')
        self.inc(2)       
        for k, v in obj.items():
            self.put('\n')
            self.indent()
            self.put(k + ': ')

            self.inc(len(k) + 2)
            self.print(v)
            self.dec()
    
        self.dec()
        self.put('\n')
        self.indent()
        self.put('}')

    def print_numeric(self, num):
        self.put(str(num))

    def print_bool(self, b):
        if b:
            self.put('true')
        else:
            self.put('false')

    def print_null(self, n):
        self.put('null')

    def print_string(self, string):
        self.put('"' + self.escape(string) + '"')

    def escape(self, s):
        ret = ''
        escape = { '\t' : '\\t'
                 , '\n' : '\\n'
                 , '\r' : '\\r'
                 , '\d' : '\\d'
                 , '\f' : '\\f'
                 , '"'  : '\\"'
                 , '\\' : '\\\\' }
        for c in s:
            try:
                ret += escape[c]
            except:
                ret += c
        return ret

    def dump(self):
        self.print(self.shaun)
        return self.fs
