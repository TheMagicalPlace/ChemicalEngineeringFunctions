'''
This file uses the mccabe-thiele method to grsphicslly estimate the number of stages for a trayed distillation colunm
given an array of x-data and y-data, the desired distillate and bottoms composition, and any side streams and their exiting
composition.



'''

from numpy import array,interp,append,delete,where
from matplotlib import pyplot as plot

class MTMethod():
    # TODO - impliment partial condensers -- refer to seps book for information

    def __init__(self,xdata,ydata,dfrac,bfrac,feed,feed_composition,liquid_frac_feed,reflux_ratio):
        self.xydata = array([xdata, ydata])
        self.R = reflux_ratio
        self.feed_line = []
        # TODO add a way to deal with sidestreams (incl. all liquid, all vapor, etc.)
        # for this, consider requiring an order for sidestreams and feeds,
        # i.e. [(distillate),Feed1,side1,side2,feed2...(bottoms)]

        self.feed_flow_composition_and_state = [[a, b, c] for a, b, c in zip(feed,feed_composition,liquid_frac_feed)]

        self.db_fracs = [dfrac,bfrac]
        self.distillate = sum([((feed_composition-bfrac)/(dfrac-bfrac))*feed
                              for feed,feed_composition,_ in self.feed_flow_composition_and_state])
        self.bottoms = sum(feed)-self.distillate

        self.line45 = array([x/100 for x in range(1,101)])
        self.mass_balance()
        self.find_feed_lines()

    def tray_finder(self):
        #TODO update this to work with how the rest is structured
        tray_compositions = array([[self.distillate_fraction,self.distillate_fraction]])


        while tray_compositions[-1,1] > self.bottoms_fraction:
            for fcomp in feed_composition:
                if tray_compositions[-1,0] > self.intersectt[0]:
                    tray_compositions = append(tray_compositions, array([[interp(tray_compositions[-1, 1],
                                                                                 self.xydata[1], self.xydata[0]),
                                                                          tray_compositions[-1, 1]]]), axis=0)
                    plot.plot([tray_compositions[-2, 0], tray_compositions[-1, 0]],
                             [tray_compositions[-1, 1], tray_compositions[-1, 1]])

                    tray_compositions = append(tray_compositions, array([[tray_compositions[-1, 0],
                                               interp(tray_compositions[-1, 0],self.line45,self.stripping_line)]]), axis=0)


                    plot.plot([tray_compositions[-2, 0], tray_compositions[-2, 0]],
                              [tray_compositions[-1, 1], tray_compositions[-2, 1]])
            else:

                tray_compositions = append(tray_compositions, array([[interp(tray_compositions[-1, 1],
                                                                             self.xydata[1], self.xydata[0]),
                                                                      tray_compositions[-1, 1]]]), axis=0)
                plot.plot([tray_compositions[-2, 0], tray_compositions[-1, 0]],
                         [tray_compositions[-1, 1], tray_compositions[-1, 1]])

                tray_compositions = append(tray_compositions, array([[tray_compositions[-1, 0],
                                           interp(tray_compositions[-1, 0],self.line45,self.rectifying_line)]]), axis=0)

                plot.plot([tray_compositions[-2, 0], tray_compositions[-2, 0]],
                          [tray_compositions[-1, 1], tray_compositions[-2, 1]])

        print(tray_compositions,len(tray_compositions)//2)

    def mass_balance(self):

        self.L = [self.R*self.distillate] # Liquid outflow from condenser (assumed saturated liquid)
        self.V = [self.L[0]+self.distillate] # Vapor entering into condenser
        for feed, _, q in self.feed_flow_composition_and_state:
            self.L.append(sum(self.L)+feed*q)
            self.V.append(sum(self.V)-feed*(1-q))

    def find_operating_lines(self):

        self.BoilupRatio = self.V[-1] / self.bottoms
        self.stripping_line = [self.R / (1 + self.R) * x / 100
                                     + self.db_fracs[0] / (self.R + 1) for x in range(1, 101)]
        self.rectifying_line = [(self.BoilupRatio + 1) / self.BoilupRatio * x / 100
                                      - self.db_fracs[1] / self.BoilupRatio for x in range(1, 101)]
        operating_lines = [self.stripping_line,self.rectifying_line]
        if len(self.L) and len(self.V) > 2:
            for L,V in self.L[1:-1],self.V[1:-1]:
                pass
        for op_line in operating_lines:
            if operating_lines[0] == op_line[0]:
                self.find_operating_line_intersection(op_line,self.feed_line[0])
            elif operating_lines[-1] == op_line[0]:
                self.find_operating_line_intersection(op_line, self.feed_line[-1])




    def find_feed_lines(self):
        self.feed_equilibrium_intersect = array([[1,1]])
        for _,zF,q in self.feed_flow_composition_and_state:
            q_line = array([q/ (q - 1) * x / 100
             - (zF / (q - 1)) for x in range(1, 101)])
            for i in range(1,1001):
                i = i/1000
                q_cord = interp(i,self.line45,q_line)
                eqcord = interp(i,self.xydata[0],self.xydata[1])
                print(abs(q_cord-eqcord))
                if abs(q_cord-eqcord) < 0.005:
                    x = interp(q_cord,self.xydata[1],xydata[0])
                    self.feed_equilibrium_intersect = append(self.feed_equilibrium_intersect,array([[x, eqcord]]),axis = 0)
                    break
            self.feed_line.append(q_line)
        self.feed_equilibrium_intersect = delete(self.feed_equilibrium_intersect,0)
        self.feed_equilibrium_intersect = delete(self.feed_equilibrium_intersect, 0)

    def find_operating_line_intersection(self,operating_line_1,feed_line):

        for i in range(1, 1001):
            i = i / 1000
            line1cord = interp(i, self.line45, operating_line_1)
            line2cord = interp(i, self.line45, feed_line)
            diff = abs(line1cord-line2cord)
            if diff < 0.005:
                x = interp(line1cord, operating_line_1, self.line45)
                return x,line1cord

    def graph_generator(self):
        mt_plot = plot.figure()
        self.tray_finder()
        plot.plot(self.line45,self.line45)
        plot.plot([self.feed_comp,self.eqint[0]],[self.feed_comp,self.eqint[1]])
        plot.plot([self.dbfracs[1],self.intersectb[0]],[self.dbfracs[1],self.intersectb[1]])
        plot.plot([self.intersectt[0], self.dbfracs[0]], [self.intersectt[1], self.dbfracs[0]])
        plot.plot(self.xydata[0],self.xydata[1])
        plot.show()





#Testing values

xydata = [list(x) for x in zip
(*[[0.00350, 	0.02050],
[0.00450, 	0.02750],
[0.01750, 	0.13150],
[0.05850, 	0.30500],
[0.06800, 	0.36150],
[0.09350, 	0.41100],
[0.16500, 	0.52000],
[0.21250, 	0.54550],
[0.24100, 	0.56750],
[0.36150, 	0.60600],
[0.47400, 	0.65050],
[0.49850, 	0.65550],
[0.58150, 	0.69700],
[0.64600, 	0.72900],
[0.65400, 	0.73100],
[0.72300, 	0.77600],
[0.79000, 	0.82000],
[0.83700, 	0.85200],
[0.87310, 	0.88170],
[0.88300, 	0.88850],
[0.88800, 	0.89300],
[0.89730, 	0.90120],
[0.94890, 	0.95020],
[0.97070, 	0.97150],
[0.98250, 	0.98350]])]

distillate_fraction = 0.85
bottoms_fraction = 0.05
feed = [100]
feed_composition = [0.6]
liquid_composition = [0.5]
relfux_ratio = 1.6
print(xydata[0])
test = MTMethod(xydata[0],xydata[1],distillate_fraction,bottoms_fraction,feed,feed_composition,liquid_composition,relfux_ratio)
test.find_operating_lines()
test.graph_generator()

