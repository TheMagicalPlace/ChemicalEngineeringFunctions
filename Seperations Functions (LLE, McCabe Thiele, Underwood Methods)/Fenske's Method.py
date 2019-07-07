'''
This file finds the minimum number of stages for a plate distillation colunm using Fenske's Method, and can be used
for both type I & II underwood seperations
'''


class FUGMethod:
    import numpy as np
    from math import fabs,exp,log,log10,pow,sqrt,sin,cos,tan,pi,e

    def __init__(self):
        self.keys = [1, 2]
        self.alpha_vals = []
        self.feed_flow = 0
        self.isclassI = True

    def outlet_flow_rates(self,flow,split_fraction):
        if self.isclassI == True:
            distillate = [flow[x] if x < self.keys[1]  else 0 for x in range(0,len(flow))]
            bottoms = [flow[x] if x > self.keys[0] else 0 for x in range(0,len(flow))]
            print(distillate, bottoms)
            distillate[self.keys[0]],distillate[self.keys[1]] = split_fraction[0] * flow[self.keys[0]],\
                                                   (1-split_fraction[1]) * flow[self.keys[1]]
            bottoms[self.keys[0]],bottoms[self.keys[1]] = (1-split_fraction[0]) * flow[self.keys[0]],\
                                                   split_fraction[1] * flow[self.keys[1]]
            self.outlet = [distillate,bottoms]

    def find_alphas


intt = FUGMethod()

intt.outlet_flow_rates([10,20,20,50],[.99,.98])