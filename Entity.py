class Entity:

    def __init__(self, *args):
        self.date = args[0][0]
        self.open_val = args[0][1]
        self.high = args[0][2]
        self.low = args[0][3]
        self.close = args[0][4]
        self.adj_close = args[0][5]
        self.volume = args[0][6]

    def __str__(self):
        return f'{self.date}|{self.open_val}|{self.high}|{self.low}|{self.close}|{self.adj_close}' \
               f'|{self.volume}'
