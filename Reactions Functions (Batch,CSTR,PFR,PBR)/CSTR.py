
from typing import List
from scipy.optimize import fsolve

import scipy.integrate as intgr

from scipy.integrate import solve_ivp

import matplotlib.pyplot as plt
from numpy import log10, log2, log,percentile
from typing import List
from numpy import linspace
from collections import defaultdict
class RateLawContainer():

    labels = (lab for lab in ('Ca', 'Cb', 'Cc', 'Cd', 'Ce','Cf','Cg'))
    index = (i for i in range(10))

    def __init__(self,initial_concentration,st_ratios,comp_ratios,rxn_coefficient : int,k_forward=None,k_reverse=None):
        self.rxn_coefficient = rxn_coefficient
        self.st_ratios = st_ratios
        self.comp_ratios = comp_ratios
        self.label = next(RateLawContainer.labels)
        self.index = next(RateLawContainer.index)
        self.C0 = initial_concentration


        self.generated_by = []
        self.same_level = []
        self.k_forward = k_forward
        self.k_reverse = k_reverse


    def generate_rate_law(self):
        if self.k_forward:
            odebase = f'{self.k_forward}*(-1)*(1'
            base = f'{self.k_forward}*(-1)*(1'
            for node in self.same_level:
                base+=f'*({self.C0}*({self.comp_ratios[node.index]}-{self.st_ratios[node.index]}*X))**{abs(node.rxn_coefficient)}'
                odebase += f'*{node.label}**{abs(node.rxn_coefficient)}'
            if self.generated_by:

                base+=f'-{1/self.generated_by[0].k_reverse}'
                odebase+=f'-{1/self.generated_by[0].k_reverse}'
            for node in self.generated_by:
                base+=f'*({self.C0}*({self.comp_ratios[node.index]}-{self.st_ratios[node.index]}*X))**{abs(node.rxn_coefficient)}'
                odebase += f'*{node.label}**{abs(node.rxn_coefficient)}'
            base+=')';odebase+=')'

        self.reaction = base
        self.odebase = odebase
        self._set_rate_law_ratios()

    def _set_rate_law_ratios(self):
        for node in self.same_level:
            if node.generated_by == self.generated_by and node.same_level == self.same_level:
                node.reaction = f'({node.rxn_coefficient/self.rxn_coefficient})*{self.reaction}'
                node.odebase = f'({node.rxn_coefficient/self.rxn_coefficient})*{self.odebase}'
        for node in self.generated_by:
            if node.generated_by == self.same_level:
                node.reaction = f'({node.rxn_coefficient / self.rxn_coefficient})*{self.reaction}'
                node.odebase = f'({node.rxn_coefficient / self.rxn_coefficient})*{self.odebase}'
    def __eq__(self, other):
        return self.label == other

class CSTRABC():

    def __init__(self,component_flows,stoicheometry):
        self.components = component_flows
        self.vol_flow = sum(component_flows)
        self.stoicheometry = stoicheometry
        self.C0_components = [flow/self.vol_flow for flow in self.components]
        self.comp_ratios = [comp/self.components[0] for comp in self.components]
        self.st_ratios = [st/self.stoicheometry[0] for st in stoicheometry]


class CSTRAnalysis(CSTRABC):

    def __init__(self,component_flows : List[int],stoicheometry : List[int],
                 reaction_rate : int = None,volume : List[int] = None,
                 conversion_range : List[int] = None):

        super().__init__(component_flows,stoicheometry)
        self.rA = reaction_rate

    def sizing(self, conversion,rxn_rate):
        X = conversion/100 # % conversion
        volume = self.C0_components[0]*self.vol_flow*X/(-rxn_rate)
        return volume
        #vol/C0*vol_flow

class CSTRDesigner(CSTRABC,):

    def __init__(self,component_flows,stoicheometry,k_forward: List[int] = None,
                 k_reverse: List[int] = None, layers: List[List[int]] = None):

        super().__init__(component_flows,stoicheometry)

        j = 0
        if layers and k_forward and k_reverse:
            species = [[] for _ in range(len(layers))]
            for i,layer in enumerate(layers):
                for comp_mass in layer:
                    j +=1
                    if i > 0:
                        new_node = RateLawContainer(comp_mass , rxn_coefficient=self.stoicheometry[j],st_ratios=self.st_ratios,
                                                    comp_ratios=self.comp_ratios,k_forward=k_forward[j], k_reverse=k_reverse[j])

                        for node in species[i-1]:
                            if node.k_foreward:
                                new_node.generated_by.append(node)
                                if new_node.k_reverse:
                                    node.generated_by.append(new_node)

                    else:
                        new_node = RateLawContainer(comp_mass, rxn_coefficient=self.stoicheometry[j],
                                                    st_ratios=self.st_ratios,
                                                    comp_ratios=self.comp_ratios, k_forward=k_forward[j],
                                                    )
        else:
            react, product = [], []
            for i,spec in enumerate(self.C0_components):
                if stoicheometry[i] < 0:
                    product.append(RateLawContainer(spec , rxn_coefficient=stoicheometry[i],st_ratios=self.st_ratios,
                                                    comp_ratios=self.comp_ratios,k_reverse=k_reverse[i]))
                else:
                    react.append(RateLawContainer(spec , rxn_coefficient=stoicheometry[i],st_ratios=self.st_ratios,
                                                    comp_ratios=self.comp_ratios, k_forward=k_forward[i]))
            else :
                for node in react:
                    node.same_level = react
                    node.generates = product
                    for pnode in product:
                        pnode.generated_by.append(node)
                        if pnode.k_reverse:
                            pnode.same_level = product
                            node.generated_by.append(pnode)
            self.RL_nodes = react+product
        self.RL_nodes[0].generate_rate_law()


    def sizing(self, conversion):
        X = conversion/100 # % conversion
        rA = eval(f'{self.RL_nodes[0].reaction}')
        volume = self.vol_flow*self.C0_components[0]*(1-X)/(-rA)
        return volume,rA

    def find_conversion(self,volume):
        base = f'-{self.C0_components[0] * self.vol_flow}*X/({self.RL_nodes[0].reaction})-{volume}'
        #zfun = None

        exec(f'zfun = lambda X : {base}',None,locals())
        loc = locals()
        zfunc = loc['zfun']
        X = 'X'
        z =fsolve(zfunc,0.01)
        return z

    def _ode_constructor(self):
        Z = {}
        K = {}
        # Ca + Cb + Cc = Ca0 + Cb0 + Cc0
        labels = ['Ca','Cb','Cc','Cd','Ce']

        laws = {}
        for i, c in enumerate(self.RL_nodes):
            laws[f'd{c.label}dt'] = f'{c.reaction}*{self.C0_components[i]}'
        print(laws)

        def for_ode(X,C):
            for i,c in enumerate(C):
                label = labels[i]
                exec(f'{label} = c')
            C = []
            for name,reaction in laws.items():
                exec(f'C.append({reaction})')


            return C
        return for_ode

    def solve_ode(self):
        ivp_fun = self._ode_constructor()
        result = solve_ivp(ivp_fun, t_span=
        (0,0.9), y0=self.C0_components, method='RK45', t_eval=[n/100 for n in range(0,91)], dense_output=False, events=None,ectorized=False)
        res = result.y

        fig = plt.figure()
        axa,axb = fig.subplots(2)
        for num,ii in enumerate(res):
            iii = [self.vol_flow*c for c in ii]
            axa.plot(result['t'],iii)
            axa.legend(['A','B','C','D'])
        axb.plot(result.t,[(self.C0_components[0]-C)/self.C0_components[0] for C in res[0]])
        plt.show()
        print('')


if __name__ == '__main__':
    btchr = CSTRDesigner(component_flows=[50, 100,20, 20],
                         stoicheometry=[2, 1, -1, -2], k_forward=[100,100,None,None], k_reverse=[None,None,10,10it g])
    #btchr.solve_ode()
    print(btchr.sizing(50))

    x = [i for i in range(10,2000,20)]
    y = [j for j in range(5,90)]
    q = []
    volume = [];rate = []
    voverr = []
    fig = plt.figure()
    ax1,ax2,ax3 = fig.subplots(3)
    for i in x:
        q.append(btchr.find_conversion(i))

    for i in y:
        e  = (btchr.sizing(i))
        volume.append(e[0]),rate.append(e[1])
    for v,r in zip(volume,rate):
        voverr.append(-v/r)
    ax1.scatter(x,q)
    ax2.scatter(y,rate)
    ax3.scatter(y,[-50/r for r in rate])
    #ax2.scatter(y,volume)
    #ax3.set_ylim(top=percentile(voverr,97),bottom=percentile(voverr,3))
    ax3.set_xlim(left=0)
    ax3.set_ylim(bottom=0,top=percentile([-50/r for r in rate],95))
    plt.show()
    #btchr.solve_ode()