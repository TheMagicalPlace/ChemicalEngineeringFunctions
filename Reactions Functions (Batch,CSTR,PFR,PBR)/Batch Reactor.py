import scipy.integrate as intgr

from scipy.integrate import solve_ivp

import matplotlib.pyplot as plt
from numpy import log10, log2, log,percentile
from typing import List
from numpy import linspace
from collections import defaultdict
class RateLawContainer():

    labels = (lab for lab in ('Ca', 'Cb', 'Cc', 'Cd', 'Ce','Cf','Cg'))


    def __init__(self,initial_concentration,rxn_coefficient,volume,system_mass,k_forward=None,k_reverse=None):
        self.label = next(RateLawContainer.labels)
        self.C0 = initial_concentration
        self.generated_by = []

        self.same_level = []
        self.k_forward = k_forward
        self.k_reverse = k_reverse
        self.rxn_coefficient = rxn_coefficient
        self.N = system_mass

    def generate_rate_law(self):
        if self.k_forward:
            base = f'{self.k_forward}*(-1)*(1'
            for node in self.same_level:
                base+=f'*{node.label}**{abs(node.rxn_coefficient)}'
            if self.generated_by:
                base +='-'
                base+=f'{1/self.generated_by[0].k_reverse}'
            for node in self.generated_by:
                base+=f'*{node.label}**{abs(node.rxn_coefficient)}'
            base+=')'
        self.reaction = base
        self._set_rate_law_ratios()

    def _set_rate_law_ratios(self):
        for node in self.same_level:
            if node.generated_by == self.generated_by and node.same_level == self.same_level:
                node.reaction = f'({node.rxn_coefficient/self.rxn_coefficient})*{self.reaction}'
        for node in self.generated_by:
            if node.generated_by == self.same_level:
                node.reaction = f'({node.rxn_coefficient / self.rxn_coefficient})*{self.reaction}'

    def __eq__(self, other):
        return self.label == other
class BatchReactorABC():

    def __init__(self,species_data,stoicheometry):
        self.species_data = species_data
        self.N = sum(species_data)
        self.Na0 = species_data[0]
        self.stoicheometry = stoicheometry

    def species_concentration(self, conversion,volume=None):

        Cval = 100
        C = f'{Cval}'
        K = f'{Cval} / 10'
        sig = self.stoicheometry

        # Ca0*(b/a-X*(s_b/s_a))
        if  not volume:
            volume = 100
        for i in range(0, len(self.species_data)):
            if self.stoicheometry[i] > 0:
                # ...* (Na0*(Ni0/Na0-(a/i)*x)/volume)**i

                # C = ...*(Na0*(1-X)/volume
                C+= f"*({self.Na0/volume}*({self.species_data[i]/self.species_data[0]}-{sig[i] / sig[0]}*x))**{abs(self.stoicheometry[i])}"
            else:
                K+= f"*({self.Na0/volume}*({self.species_data[i]/self.species_data[0]}-{sig[i] / sig[0]}*x))**{abs(self.stoicheometry[i])}"


        new_species_data = list(range(len(self.species_data)))
        for i,species in enumerate(self.species_data):
            new_species_data[i] = self.Na0*(self.species_data[i]/self.species_data[0]-sig[i]/sig[0]*conversion/100)
        self.species_data = new_species_data

        x = conversion/100
        self.rA = -(eval(C)-eval(K))
        Z = f'-({C}-{K})'


        Ntime = [];Nsize = []
        #for vol in [20,40,80,160,320,640,1280]:
        #    Ntime.append(self.time_to_conversion(conversion/100,volume=vol))
        #    Nsize.append(self.sizing(conversion=conversion/100, duration=vol))


        #return new_species_data,intgr.quad(self.test, 0, conversion/100, args=Z),self.rA,Ntime,Nsize

class BatchReactorAnalysis(BatchReactorABC):

    def __init__(self,species_data,stoicheometry,rate_coeffieients,volume : List[int]=None,conversion_range : List[int] = None,run_time_range : List[int] = None):

        super().__init__(species_data,stoicheometry)
        self.rA = -rate_coeffieients[0]

        if not volume:
            volume = defaultdict(list)
            if len(conversion_range) == 1:

                if len(run_time_range) == 1:
                    volume = self.sizing(conversion_range[0],run_time_range[0])
                else:
                    volume = []
                    run_points = linspace(start=run_time_range[0],stop=run_time_range[1],endpoint=True,num=10)
                    for run_time in run_points:
                        volume.append(self.sizing(conversion_range[0],run_time))
                    self.plot_data(run_points,volume)
            else:
                conv_points = linspace(start=conversion_range[0], stop=conversion_range[1], endpoint=True, num=10)

                if len(run_time_range) == 1:
                    volume = []
                else:
                    run_points = linspace(start=run_time_range[0], stop=run_time_range[1], endpoint=True, num=10)
                for conv in conv_points:
                    if len(run_time_range)== 1:
                        volume.append(self.sizing(conv,run_time_range[0]))
                    else:
                        for run_time in run_points:
                            volume[conv].append(self.sizing(conv,run_time))
                if isinstance(volume,list):
                    self.plot_data(conv_points, volume)
                else:
                    self.plot_data(volume,run_points)

        if not run_time_range:
            run_time = defaultdict(list)
            if len(conversion_range) == 1:
                if len(volume) == 1:
                    run_time = self.time_to_conversion(conversion_range[0], volume[0])
                else:
                    run_time = []
                    volume_points = linspace(start=volume[0], stop=volume[1], endpoint=True, num=10)
                    for vol in volume_points:
                        run_time.append(self.time_to_conversion(conversion_range[0], vol))
                    self.plot_data(run_time,volume)
            else:
                conv_points = linspace(start=conversion_range[0], stop=conversion_range[1], endpoint=True, num=10)

                if len(volume) == 1:
                    run_time = []
                else:
                    volume_points = linspace(start=volume[0], stop=volume[1], endpoint=True, num=10)
                for conv in conv_points:
                    if len(volume) == 1:
                        volume.append(self.time_to_conversion(conv, volume[0]))
                    else:
                        for vol in volume_points:
                            run_time[conv].append(self.time_to_conversion(conv, vol))
                if isinstance(run_time,list):
                    self.plot_data(run_time, conv_points)
                else:
                    self.plot_data(run_time, volume_points)

        self.run_time_range = run_time_range
        conversion = None
        if not conversion_range:
            conversion = defaultdict(list)
            if len(run_time_range) == 1:
                if len(volume) == 1:
                    conversion = self.get_possible_conversion(volume[0],run_time_range[0])
                else:
                    conversion = []
                    volume_points = linspace(start=volume[0], stop=volume[1], endpoint=True, num=10)
                    for vol in volume_points:
                        conversion.append(self.get_possible_conversion( vol,run_time_range[0]))
            else:
                run_points = linspace(start=run_time_range[0],stop=run_time_range[1],endpoint=True,num=10)

                if len(volume) == 1:
                    conversion = []
                else:
                    volume_points = linspace(start=volume[0], stop=volume[1], endpoint=True, num=10)
                for run_time in run_points:
                    if len(volume) == 1:
                        conversion.append(self.get_possible_conversion(volume[0],run_time))
                    else:
                        for vol in volume_points:
                            conversion[run_time].append(self.time_to_conversion(vol,run_time))
        self.conversion_range = conversion if conversion else conversion_range

    def sizing(self, conversion, duration):
        X = conversion # % conversion
        Na0 = self.Na0 # moles of species 0

        dX = intgr.quad(lambda x:x, 0, X)[0] # intergral d/dX
        Volume = -Na0 * dX / (duration * self.rA)
        self.species_concentration(conversion,Volume)
        Volume = -Na0 * dX / (duration * self.rA)
        return Volume

    def time_to_conversion(self, conversion, volume):

        X, V, Na0 = conversion, volume, self.Na0
        dX = intgr.quad(lambda x:x, 0, X)[0]
        self.species_concentration(conversion,volume)
        time = -Na0 * dX /(self.rA * V)
        print(time,V,self.rA,dX,Na0)
        return time

    def get_possible_conversion(self,volume,duration):
        t, V, Na0 = duration, volume, self.Na0
        return duration*self.rA*V/(-Na0)

    def plot_data(self,x,y=None):
        if isinstance(x,list):
            fig = plt.figure()
            ax = fig.subplots(1)
            ax.scatter(x,y)
        else:
            fig = plt.figure()
            ax,ax2 = fig.subplots(2)
            for key,value in x.items():
                print(value)
                ax.plot(y,value)

                ax2.plot(value,list(x.keys()))
            ax.legend([f'{str(key)[:2]}' for key in x.keys()])
            ax2.legend([f'{str(key)[:2]}' for key in x.keys()])
            plt.show()

class BatchReactorODE(BatchReactorABC):

    def __init__(self, species_data, stoicheometry, volume,k_forward : List[int],k_reverse: List[int],layers:List[List[int]]=None):
        super().__init__(species_data,stoicheometry)
        self.volume = volume
        species = []
        j = 0
        if layers and k_forward and k_reverse:
            species = [[] for _ in range(len(layers))]
            for i,layer in enumerate(layers):
                for comp_mass in layer:
                    j +=1
                    if i > 0:
                        new_node = RateLawContainer(comp_mass / volume, stoicheometry[i], volume, sum(species),
                                                    k_forward=k_forward[j], k_reverse=k_reverse[j])

                        for node in species[i-1]:
                            if node.k_foreward:
                                new_node.generated_by.append(node)
                                if new_node.k_reverse:
                                    node.generated_by.append(new_node)

                    else:
                        new_node = RateLawContainer(comp_mass / volume, stoicheometry[i], volume, sum(species),
                                                    k_forward=k_forward[j])
        else:
            react, product = [], []
            for i,spec in enumerate(species_data):
                if stoicheometry[i] < 0:
                    product.append(RateLawContainer(spec / volume, stoicheometry[i], volume, sum(species),k_reverse=k_reverse[i]))
                else:
                    react.append(RateLawContainer(spec / volume, stoicheometry[i], volume, sum(species), k_forward=k_forward[i]))
            else :
                for node in react:
                    node.same_level = react
                    node.generates = product
                    for pnode in product:
                        pnode.generated_by.append(node)
                        if pnode.k_reverse:
                            pnode.same_level = product
                            node.generated_by.append(pnode)
            species = react+product

        self.RL_nodes = species
        self.rate_laws()
        self.solve_ode()



    def rate_laws(self):
        self.RL_nodes[0].generate_rate_law()
        print(self.RL_nodes)

    def _time_integral(self):
        Z = {}
        K = {}
        # Ca + Cb + Cc = Ca0 + Cb0 + Cc0
        labels = ['Ca','Cb','Cc','Cd','Ce']

        laws = {}
        for i, c in enumerate(self.RL_nodes):
            laws[f'd{c.label}dt'] = f'{c.reaction}'
        print(laws)

        def for_ode(t,C):
            for i,c in enumerate(C):
                label = labels[i]
                exec(f'{label} = c')
            C = []
            for name,reaction in laws.items():
                #exec(f'{name} = None')
                C.append(eval(reaction))

            return C
        return for_ode

    def solve_ode(self):
        ivp_fun = self._time_integral()
        C0 = [data/self.volume for data in self.species_data]

        t = solve_ivp(ivp_fun, t_span=(0.0,1000.0), y0=C0, method='RK45', t_eval=None, dense_output=False, events=None,ectorized=False)
        res = t.y
        N = sum(self.species_data)
        fig = plt.figure()
        axa,axb = fig.subplots(2)
        for num,ii in enumerate(res):
            iii = [c*N for c in ii]
            axa.plot(t.t,iii)
        axb.plot(t.t,[(C0[0]-C)/C0[0] for C in res[0]])
        plt.show()
        print('')



class BatchReactorMeta:
    """Initializes the pertinent batch reactor class"""

    def __init__(self, species_data, stoicheometry, rxn_rates=None,conversion_factor :List[int] = None, volume=None, k_forward: List[int] = None,
                 k_reverse: List[int] = None, layers: List[List[int]] = None):
        if conversion_factor and not volume:
            pass


if __name__ == '__main__':
    kf = 11
    kr = 1005
    btr = BatchReactorAnalysis(species_data=[50, 100, 50, 10],
                         stoicheometry=[2, 1, 1, -2],rate_coeffieients=[10, 1, 1, 1],conversion_range=[10,90],run_time_range=[10,1000])
    btchr = BatchReactorODE( species_data=[50, 50, 50, 50],
                         stoicheometry=[2, 1, 0, -3], k_forward=[kf,kf,None,None],
                         k_reverse=[None,None,kr,kr],volume=700)

if __name__ == '':

    btchr = BatchReactor(rxn_rates=[1, 1, 1, 1], species_data=[200, 100,0, 0],
                     stoicheometry=[2, 1, -1, -2], rate_law_constant=1, volume=1000)

    btchr.solve_ode()
    btchr.time_integral()
    print(btchr.rate_laws())

    ax,bx,cx,dx = [],[],[],[]
    size,timesize = [],[]
    rxnlaws = []
    x0 = 1
    is_possible = 0
    for xy in range(x0, 99):

        conc_data,rxn_data,rate,timeforvol,volfortime = btchr.species_concentration(xy)
        a,b,c,d = conc_data
        ax.append(a);bx.append(b);cx.append(c);dx.append(d);
        size.append(volfortime);rxnlaws.append(rate);timesize.append(timeforvol)
        if rate > 0 and not is_possible:
            is_possible = xy/100


    size = zip(*size)
    timesize = zip(*timesize)
    fig = plt.figure()
    ax1,ax2 = fig.subplots(2,2,sharex=True)
    axc,axd = ax1
    axb,axa = ax2
    axis = [(x0+x)/100 for x in range(len(rxnlaws))]


    axa.scatter(axis, ax)
    axa.scatter(axis,bx)

    #axc.set_xscale('linear')
    axb.set_xlim(left=0,right=1)
    axc.set_xlim(left=0, right=1)
    axa.set_xlim(left=0,right=1)
    axd.set_xlim(left=0,right=1)



    for volume in [20,40,80,160,320,640,1280]:
        x = [-conv/(rxn*volume) for rxn,conv in zip(rxnlaws,axis)]
        a = [axs for axs in axis]
        axb.set_ylim(top=percentile(x,97),bottom=0)
        axb.scatter(a,x)
    axb.legend([f'Time Required at Volume {x}' for x in [20,40,80,160,320,640,1280]])

    for s in timesize:
        s = [s for s in s]
        a = [axs for axs in axis]
        axc.scatter(a,s)
        axc.set_ylim(top=percentile(s,97), bottom=0)
    axc.legend([f'Volume for Conversion at T {x}' for x in [20,40,80,160,320,640,1280]])

    rxnlaws = [rxn for rxn in rxnlaws]

    axd.scatter(axis,rxnlaws)
    for i in range(int(is_possible*100),200,2):
        axa.axvline(x=i/100,linestyle='dashdot',color='r')
        axb.axvline(x=i/100,linestyle='dashdot',color='r')
        axc.axvline(x=i/100,linestyle='dashdot',color='r')
        axd.axvline(x=i/100,linestyle='dashdot',color='r')

    axc.set_yscale('linear')
    axb.set_yscale('linear')


    axa.scatter(axis, cx)
    axa.scatter(axis, dx)
    axa.legend(['a', 'b', 'c', 'd'])
    axa.set_ylim(bottom=0)
    axd.set_ylim(top=0.1)

    axd.vlines(x=[i/100 for i in range(101)],ymin=0,ymax=0.1,linestyle='dashdot',color='r')
    plt.show()
