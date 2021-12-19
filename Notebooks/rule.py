class Rule:
    def __init__(self, rule, args=None):
        self.rule = rule
        self.args = args
        self.terms = [t.split(' ') for t in self.rule.split(' and ')]
        self.agg_dict = {}
        self.factorize()
        self.rule = str(self)
  

    def factorize(self):
        for feature, symbol, value in self.terms:
            if (feature, symbol) not in self.agg_dict:
                if symbol != '==':
                    self.agg_dict[(feature, symbol)] = str(float(value))
                else:
                    self.agg_dict[(feature, symbol)] = value
            else:
                if symbol[0] == '<':
                    self.agg_dict[(feature, symbol)] = str(min(
                                float(self.agg_dict[(feature, symbol)]),
                                float(value)))
                elif symbol[0] == '>':
                    self.agg_dict[(feature, symbol)] = str(max(
                                float(self.agg_dict[(feature, symbol)]),
                                float(value)))
                else:  # Handle the c0 == c0 case
                    self.agg_dict[(feature, symbol)] = value
        #print(self.agg_dict)

    def __iter__(self):
        yield str(self)
        yield self.args

    def __repr__(self):
        return ' and '.join([' '.join(
                [feature, symbol, str(self.agg_dict[(feature, symbol)])])
                for feature, symbol in sorted(self.agg_dict.keys())
                ])