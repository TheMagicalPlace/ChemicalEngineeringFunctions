'''
This file finds the minimum number of stages for a plate distillation colunm using Fenske's Method, and can be used
for both type I & II underwood seperations
'''

from math import log10, pow, sqrt, isclose
class FUGMethod:

    def __init__(self, feed, keys):
        self.keys = keys
        # self.isclassII = True
        # self.alpha= []
        # self.distillate = []
        # self.bottoms = []
        # self.mfrac_bottoms= []
        # self.mfrac_distillate = []
        # self.mfrac_feed = []
        self.feed = feed
        self.classIItest = []

    def variations_for_convenience(self):
        # These are just so as to avoid repeatedly defining mole fractions and sums in unrelated methods

        # sum of distillate, bottoms, and feed respectivlly
        self.F, self.D, self.B = sum(self.feed), sum(self.distillate), sum(self.bottoms)

        # mole fractions
        self.molefrac_distillate = [x / self.D for x in self.distillate]
        self.molefrac_bottoms = [x / self.B for x in self.bottoms]
        self.molefrac_feed = [x / self.F for x in self.bottoms]

    def outlet_flow_rates(self, split_fraction):
        distillate = [self.feed[x] if x < self.keys[1] else 0 for x in range(0, len(self.feed))]
        bottoms = [self.feed[x] if x > self.keys[0] else 0 for x in range(0, len(self.feed))]
        distillate[self.keys[0]], distillate[self.keys[1]] = round(split_fraction[0] * self.feed[self.keys[0]], 4), \
                                                             round((1 - split_fraction[1]) * self.feed[self.keys[1]], 4)
        bottoms[self.keys[0]], bottoms[self.keys[1]] = round((1 - split_fraction[0]) * self.feed[self.keys[0]], 4), \
                                                       round(split_fraction[1] * self.feed[self.keys[1]], 4)
        self.distillate, self.bottoms = distillate, bottoms
        self.variations_for_convenience()
        self.is_this_class_II()
        Nmin = self.fenske_equation()

        for i in range(0, len(self.feed)):
            if i not in self.keys:
                distillate[i] = self.feed[i] * (distillate[self.keys[1]] / bottoms[self.keys[1]]) * pow(self.alpha[i],
                                                                                                        Nmin) \
                                / (1 + (distillate[self.keys[1]] / bottoms[self.keys[1]]) * pow(self.alpha[i], Nmin))
                bottoms[i] = self.feed[i] / (
                        1 + (distillate[self.keys[1]] / bottoms[self.keys[1]]) * pow(self.alpha[i], Nmin))
            else:
                continue
            self.distillate, self.bottoms = distillate, bottoms

    # This needs to be changed to actually use K values instead of an approximation
    def find_relative_volatility(self, K_values):
        relalphas = [x / K_values[self.keys[1]] for x in K_values]
        self.alpha = relalphas

    def fenske_equation(self):
        di, dj = self.distillate[self.keys[0]], self.distillate[self.keys[1]]
        bi, bj = self.bottoms[self.keys[0]], self.bottoms[self.keys[1]]
        min_stages = log10((di / dj) * (bj / bi)) / (log10(sqrt(self.alpha[self.keys[0]])))
        return min_stages

    # modify to account for volatile components between keys
    def underwood_equation(self, feed_liquid_percent):
        q = feed_liquid_percent
        xD, xB, xF = self.molefrac_distillate, self.molefrac_bottoms, self.molefrac_feed
        if self.isclassII == False:
            keys = self.keys
            internal_reflux_ratio = q * ((self.D * xD[keys[0]] / (self.F * q * xF[keys[0]]))
                                         - self.alpha[keys[0]] * (self.D * xD[keys[1]] / (self.F * q * xF[keys[1]]))) \
                (self.alpha[0] - 1)

            reflux_ratio = internal_reflux_ratio * self.F / self.D
            print(internal_reflux_ratio, 'irr', reflux_ratio)
        else:
            f_attempt, theta, rcomp = 0, 1, 0
            while (isclose(f_attempt, self.F * q, abs_tol=0.5) != True) and (theta < self.alpha[self.keys[0]]):
                theta += 0.00001
                f_attempt = 0

                for i in range(0, len(self.feed)):
                    if self.classIItest[i] > 1:
                        f_attempt += 0
                    else:
                        f_attempt += self.alpha[i] * self.feed[i] / (self.alpha[i] - theta)

            for x in range(0, len(self.feed)):
                rcomp += self.alpha[x] * self.distillate[x] / (self.alpha[x] - theta)
            self.reflux_ratio = rcomp / self.D - 1
            print(self.reflux_ratio, rcomp)

    def is_this_class_II(self):
        keys = self.keys
        for i in range(0, len(self.feed)):
            if i not in self.keys:
                a = (self.alpha[i] - 1) / (self.alpha[keys[0]] - 1) * \
                    (self.distillate[keys[0]] / self.feed[keys[0]]) \
                    + (self.alpha[keys[0]] - self.alpha[i]) / (self.alpha[keys[0]] - 1) * \
                    (self.distillate[keys[1]] / self.feed[keys[1]])
                self.classIItest.append(a)
            else:
                self.classIItest.append(0)
        self.isclassII = True if [x for x in self.classIItest if 0 < x < 1] else False


# TODO add methods for the use of the gillerand correlation
# TODO modify the underwood equation method to account for intermediate non-keys
# TODO modify how relative volatilities are calculated to use K-values instead
# TODO allow for multiple types of input instead of just flows + keys


intt = FUGMethod([10, 40, 40, 10], [1, 2])
intt.find_relative_volatility([5, 12, 1, 1])
intt.outlet_flow_rates([.9, .9])
print(intt.fenske_equation(), 'Nmin')
intt.underwood_equation(1)
intt.is_this_class_II()


def handle(func, success=None, failure=None, exception1=0, exception2=0, exception3=0, exception4=0, *args):
    class err():
        def __init__(self, func):
            self.value = func
            pass

        def __str__(self):
            return repr(self.value)

    e = err(func)
    print((str((e.value))))

    if 1 == 2:
        if func().type != exception1:
            print('yeet')
            return failure(func, exception1)
        if func == exception2:
            return failure(func, exception2)
        if func == exception3:
            print('yeet')
            return failure(func, exception3)
        if func == exception3:
            failure(func, exception4)
        else:
            success(func, func)

    def success(func, val):
        pass

    def failure(func, exception):
        pass


onedivzero = lambda: 1 / 0
handle(onedivzero)
