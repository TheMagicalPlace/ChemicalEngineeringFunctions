import scipy.integrate as intgr


class BatchReactor:

    def __init__(self, rxn_rates, species_data, stoicheometry, rate_law_constant, volume=None):
        self.rxn_rates = rxn_rates
        self.rA = -rxn_rates[0]
        self.Na0 = species_data[0]
        self.species_data = species_data
        self.volume = volume
        self.stoicheometry = stoicheometry
        self.k = rate_law_constant
        pass

    def rate_laws(self):
        print()

    def conversion_fun(self):
        return lambda x: 1

    def sizing(self, conversion, duration):
        X = conversion
        Na0 = self.species_data[0]
        dX = intgr.quad(self.conversion_fun(), 0, X)[0]
        Volume = Na0 * dX / (duration * (-self.rA))
        return Volume

    def time_to_conversion(self, conversion, volume):
        X, V, Na0 = conversion, volume, self.species_data[0]
        dX = intgr.quad(self.conversion_fun(), 0, X)[0]
        time = Na0 * dX / (-self.rA * V)
        return time

    def test(self, X, C):
        return eval(C)

    def species_concentration(self, conversion):
        C = '1900'
        sig = self.stoicheometry
        for i in range(0, len(self.species_data)):
            if self.stoicheometry[i] > 0:
                C += '*(' + str(self.Na0) + '*(' + str((self.species_data[i] / self.Na0)) + '-' \
                     + str((sig[0]) / (sig[i])) + '*x)/' + str(self.volume) + ')**' + str(self.stoicheometry[i])
        Ca = self.species_data[0] * (1 - conversion) / self.volume
        print(C)

        print(eval(('1/(' + C + ')')))
        # C = ('1/('+C+')')
        return intgr.quad(self.test, 0, conversion, args=C)[0], self.test(conversion, C), Ca


b = BatchReactor([0, 0, 0, 0], [100, 150, 0, 0], [2, 1, -1, -1], 1, 1000)

print(b.rate_laws())
z = []
for x in range(1, 74):
    x = x / 100
    print(x)
    c, d, e = b.species_concentration(x)
    z.append([1 / (c + 0.01), 1 / d, e])
    print(z)
import matplotlib.pyplot as plot

xs = plot.figure()
plot.plot([x / 100 for x in range(1, 74)], [0 for x in z], [x / 100 for x in range(1, 74)], [0 for x in z],
          [x / 100 for x in range(1, 74)], [x[2] for x in z])
plot.show()
