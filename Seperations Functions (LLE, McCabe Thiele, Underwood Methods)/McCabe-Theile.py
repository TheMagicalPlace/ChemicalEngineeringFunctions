'''
This file uses the mccabe-thiele method to grsphicslly estimate the number of stages for a trayed distillation colunm
given an array of x-data and y-data, the desired distillate and bottoms composition, and any side streams and their exiting
composition.



'''

from numpy import array,interp,append,insert
from matplotlib import pyplot as plot

class MTMethod():

    def __init__(self,xdata,ydata,dfrac,bfrac,feed,feed_composition,lfrac_feed,reflux_ratio):
        self.xydata = array([xdata,ydata])
        self.R = reflux_ratio
        self.outfracs = [dfrac,bfrac]
        self.flows = feed*feed_composition
        self.feed_comp = feed_composition
        self.q = lfrac_feed #
        self.feed= feed
        self.distillate_fraction = dfrac
        self.bottoms_fraction = bfrac
        self.distillate = ((feed_composition-bfrac)/(dfrac-bfrac))*feed
        self.bottoms = feed-self.distillate
        self.line45 = array([x/100 for x in range(1,101)])

    def tray_finder(self):

        tray_compositions = array([[self.distillate_fraction,self.distillate_fraction]])
        print(tray_compositions)
        while tray_compositions[-1,0] > self.bottoms_fraction:
            if tray_compositions[-1,0] > self.intersectt[0]:
                print(tray_compositions)
                tray_compositions = append(tray_compositions, array([[interp(tray_compositions[-1, 1],
                                                                             self.xydata[1], self.xydata[0]),
                                                                      tray_compositions[-1, 1]]]), axis=0)
                plot.plot([tray_compositions[-1, 0], tray_compositions[-2, 0]],
                         [tray_compositions[-1, 1], tray_compositions[-1, 1]])

                tray_compositions = append(tray_compositions, array([[tray_compositions[-1, 0],
                                           interp(tray_compositions[-1, 0],self.line45,self.stripping_line)]]), axis=0)


                plot.plot([tray_compositions[-1, 0], tray_compositions[-1, 0]],
                          [tray_compositions[-2, 1], tray_compositions[-1, 1]])
            else:
                return



    def find_operating_lines(self):

        self.L0 = self.R*self.distillate
        self.V = self.L0+self.distillate
        self.Lbar = self.L0 + self.q*self.feed
        self.Vbar = self.V-self.feed*(1-self.q)
        self.BoilupRatio = self.Vbar/self.bottoms
        print(self.BoilupRatio,self.V,self.distillate)

        self.q_line = array([self.q / (self.q - 1) * x / 100
                       - (self.feed_comp / (self.q - 1)) for x in range(1, 101)])

        self.eqint=self.find_feed_equilibrium_intersection()
        print(self.eqint)


        self.stripping_line = array([self.R/(1+self.R)*x/100
                               + self.outfracs[0]/(self.R+1) for x in range(1,101)])
        self.rectifying_line = array([(self.BoilupRatio+1)/self.BoilupRatio*x/100
                                - self.outfracs[1]/self.BoilupRatio for x in range(1, 101)])

        self.intersectb = self.find_operating_line_intersection(self.rectifying_line, self.q_line)
        self.intersectt = self.find_operating_line_intersection(self.stripping_line,self.q_line)
    def find_feed_equilibrium_intersection(self):
        for i in range(1,1001):
            i = i/1000
            q_cord = interp(i,self.line45,self.q_line)
            eqcord = interp(i,self.xydata[0],self.xydata[1])
            print(abs(q_cord-eqcord))
            if abs(q_cord-eqcord) < 0.005:
                x = interp(q_cord,self.xydata[1],xydata[0])
                return x,q_cord

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
        plot.plot([self.bottoms_fraction,self.intersectb[0]],[self.bottoms_fraction,self.intersectb[1]])
        plot.plot([self.intersectt[0], self.distillate_fraction], [self.intersectt[1], self.distillate_fraction])
        #plot.plot(self.line45,self.stripping_line)
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

distillate_fraction = 0.8
bottoms_fraction = 0.05
feed = 100
feed_composition = 0.6
liquid_composition = 0.5
relfux_ratio = 2
print(xydata[0])
test = MTMethod(xydata[0],xydata[1],distillate_fraction,bottoms_fraction,feed,feed_composition,liquid_composition,relfux_ratio)
test.find_operating_lines()
test.graph_generator()

