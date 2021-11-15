from Pyro4 import expose


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        self.block_size = 256

    def solve(self):
        list_for_calc = self.read_input()
        step = int(len(list_for_calc) / len(self.workers))

        mapped = []
        for i in range(0, len(self.workers) - 1):
            mapped.append(self.workers[i].mymap((list_for_calc[i * step:i * step + step])))
        mapped.append(self.workers[len(self.workers) - 1].mymap((list_for_calc[step * (len(self.workers) - 1):])))
        print(mapped)
        self.write_output(mapped)

    @staticmethod
    @expose
    def mymap(str_list):
        rows = []
        for el in str_list:
            rows.append(Solver.bwt(str(el)))
            #rows.append(Solver.inv_bwt(str(el)))
        return rows

    @staticmethod
    @expose
    def bwt(text):
        text += '^'
        cycle_shift_table = []

        for pos in range(len(text)):
            word = text[pos:] + text[:pos]
            cycle_shift_table.append(word)

        sorted_table = sorted(cycle_shift_table)

        bwt = ''
        for row in sorted_table:
            bwt += str(row[-1])

        return bwt

    @staticmethod
    @expose
    def inv_bwt(string):
        tab = []
        for i in range(len(string)):
            tab.append('')

        for i in range(len(string)):
            for j in range(len(string)):
                tab[j] = string[j] + tab[j]
            tab = sorted(tab)

        for row in tab:
            if row[-1] == '^':
                return row[:-1]
        return ''

    def read_input(self):
        with open(self.input_file_name, 'r') as in_file:
            return self.cut_str_list(in_file.read())

    def cut_str_list(self, text):
        block = self.block_size
        return list(text[i:i+block] for i in range(0, len(text), block))

    def write_output(self, output):
        with open(self.output_file_name, 'w') as out_file:
            for i in output:
                for j in i.value:
                    out_file.write(j)



