'''
This file uses the mccabe-thiele method to grsphicslly estimate the number of stages for a trayed distillation colunm
given an array of x-data and y-data, the desired distillate and bottoms composition, and any side streams and their exiting
composition.



'''

from numpy import array,interp,append,delete,where,empty
from matplotlib import pyplot as plot

class MTMethod():
    # TODO - impliment partial condensers -- refer to seps book for information

    def __init__(self,xdata,ydata,dfrac,bfrac,feed,feed_composition,liquid_frac_feed,reflux_ratio):
        self.xydata = array([xdata, ydata])
        self.R = reflux_ratio
        self.feed_line = []
        self.op_line_intersect = []
        # TODO add a way to deal with sidestreams (incl. all liquid, all vapor, etc.)
        # for this, consider requiring an order for sidestreams and feeds,
        # i.e. [(distillate),Feed1,side1,side2,feed2...(bottoms)]

        self.feed_flow_composition_and_state = [[a, b, c] for a, b, c in zip(feed,feed_composition,liquid_frac_feed)]

        self.db_fracs = [dfrac,bfrac]
        self.distillate = sum([feed_composition*feed-feed*self.db_fracs[1]
                               for feed,feed_composition,_ in self.feed_flow_composition_and_state])/\
                                (self.db_fracs[0]-self.db_fracs[1])
        self.bottoms = sum(feed)-self.distillate
        self.line45 = array([x/100 for x in range(1,101)])
        self.mass_balance()
        self.find_feed_lines()

    def tray_finder(self):

        tray_compositions = array([[self.db_fracs[0],self.db_fracs[0]]]) # defining plate 1
        while tray_compositions[-1,0] > self.db_fracs[1]:
            for fcomp in self.op_line_intersect:
                i = self.op_line_intersect.index(fcomp)
                while tray_compositions[-1,0] > self.op_line_intersect[i][1]:

                    tray_compositions = append(tray_compositions, array([[interp(tray_compositions[-1, 1],
                                                                                 self.xydata[1], self.xydata[0]),
                                                                          tray_compositions[-1, 1]]]), axis=0)
                    plot.plot([tray_compositions[-2, 0], tray_compositions[-1, 0]],
                             [tray_compositions[-1, 1], tray_compositions[-1, 1]],color='black')

                    tray_compositions = append(tray_compositions, array([[tray_compositions[-1, 0],
                                               interp(tray_compositions[-1, 0],self.line45,self.operating_lines[i])]]), axis=0)


                    plot.plot([tray_compositions[-2, 0], tray_compositions[-2, 0]],
                              [tray_compositions[-1, 1], tray_compositions[-2, 1]],color='black')



        print(tray_compositions,len(tray_compositions)//2)

    def mass_balance(self):

        self.L = [self.R*self.distillate] # Liquid outflow from condenser (assumed saturated liquid)
        self.V = [self.L[0]+self.distillate] # Vapor entering into condenser
        for feed, _, q in self.feed_flow_composition_and_state:
            self.L.append(sum(self.L)+feed*q)
            self.V.append(sum(self.V)-feed*(1-q))
        self.V.reverse()

    def find_operating_lines(self):

        #Setting up the top-section operating line as the point to which all other operating lines are found

        self.operating_lines = [[self.R / (1 + self.R) * x / 100
                                + self.db_fracs[0] / (self.R + 1) for x in range(1, 101)]]
        self.op_line_intersect.append(self.find_operating_line_intersection(self.operating_lines[0], self.feed_line[0]))

        # This finds the 'switchover' concentration for each operating line
        # ,i.e. the concentration at which the operating line used for staging is changed
        for i in range(1,len(self.L)):
            if i != len(self.L)-1:
                int = (self.distillate * self.db_fracs[0] - self.feed_flow_composition_and_state[i][0]
                       * self.feed_flow_composition_and_state[i][1]) / self.V[i+1]
                opline = [self.L[i] / self.V[i] * ((x / 100 + self.op_line_intersect[i-1][0])
                          - self.op_line_intersect[i-1][1] + int) for x in range(1, 101)]

                self.operating_lines.append(opline)
                self.op_line_intersect.append(
                    self.find_operating_line_intersection(self.operating_lines[i], self.feed_line[i]))
            else:
                opline = [self.L[-1]/self.V[-1]* x / 100
                          - self.db_fracs[1]*(-1+self.L[-1]/self.V[-1]) for x in range(1, 101)]
                self.operating_lines.append(opline)
                self.op_line_intersect.append([self.db_fracs[1], self.db_fracs[1]])

    def find_feed_lines(self):
        for _,zF,q in self.feed_flow_composition_and_state:
            # Accounting for cases where feed is all liquid (avoiding divide by zero error)
            if q == 1:
                self.feed_line.append([zF for x in range(1,101)])
                self.feed_equilibrium_intersect = append(self.feed_equilibrium_intersect,
                                                  [[zF,interp(zF,self.xydata[0],self.xydata[1])]],axis = 0) if \
                                                  self.feed_flow_composition_and_state.index([_, zF, q]) != 0 \
                                                  else array([[zF,interp(zF,self.xydata[0],self.xydata[1])]])

                continue
            q_line = array([q/ (q - 1) * x / 100
                            - (zF / (q - 1)) for x in range(1, 101)]) if q != 1 else 0
            # To find the intersection between the feed line and the equilibrium line, an x coordinate is guessed
            # until the resultant y-values are the same
            for i in range(1,1001):
                i = i/1000
                q_cord = interp(i,self.line45,q_line)
                eqcord = interp(i,self.xydata[0],self.xydata[1])
                if abs(q_cord-eqcord) < 0.005:
                    x = interp(q_cord,self.xydata[1],xydata[0])
                    self.feed_equilibrium_intersect = append(self.feed_equilibrium_intersect,[[x, eqcord]],axis = 0) if\
                    self.feed_flow_composition_and_state.index([_,zF,q]) != 0 else array([[x, eqcord]])
                    break
            self.feed_line.append(q_line)

    def find_operating_line_intersection(self,operating_line_1,operating_line_2):

        for i in range(1, 1001):
            i = i / 1000
            line1cord = interp(i, self.line45, operating_line_1)
            line2cord = interp(i, self.line45, operating_line_2)
            t = interp(i,operating_line_2,operating_line_1)
            diff = abs(line1cord-line2cord)
            if diff < 0.005:
                x = interp(line1cord, operating_line_1, self.line45)
                return [x,line1cord]

    def graph_generator(self):
        mt_plot = plot.figure()
        self.tray_finder()
        plot.plot(self.line45,self.line45,color='blue')
        for _,z,q in self.feed_flow_composition_and_state:
            i = self.feed_flow_composition_and_state.index([_,z,q])
            plot.plot([z,self.feed_equilibrium_intersect[i][0]],[z,self.feed_equilibrium_intersect[i][1]],color = 'orange')
            plot.annotate('Feed Line #'+str(i), xy=(z, z), xytext = (z, z-0.2), arrowprops = dict(facecolor='black', shrink=0.05,width = 0.01),)
        self.db_fracs.insert(-1,interp(self.feed_flow_composition_and_state[0][1],self.xydata[0],self.xydata[1]))
        for i in range(0,len(self.operating_lines)):
        #    plot.plot([self.op_line_intersect[i-1][1],self.op_line_intersect[i][1]], [self.op_line_intersect[i][0], self.op_line_intersect[i-1][0]])
            plot.plot(self.line45,self.operating_lines[i],label='Operating Line #'+str(i))
        plot.plot(self.xydata[0],self.xydata[1],color='blue')
        plot.axis([0, 1, 0, 1])

        plot.legend()
        plot.show()
        return

        # For Testing
        c = 0
        points = []
        lines = []
        o = [b for b,c in self.op_line_intersect]
        for i in range(100,0,-1):
            e = self.operating_lines[c][i - 1]
            points.append([e, i / 100])
            if c != len(o)-1 and i/100 < o[c]:
                for j in range(i,i-10,-1):
                    e = self.operating_lines[c][j - 1]
                    points.append([e, j / 100])
                c +=1
                x = [x[::-1] for x in zip(*points)]
                plot.plot(x[1],x[0],label='Operating Line #'+str(c))
                points = []
        print(int(self.db_fracs[-1]*100))
        for k in range(int(100*self.db_fracs[-1]), int(100*self.op_line_intersect[-2][0])+10,1):
            e = self.operating_lines[-1][k-1]
            lines.append([e, k / 100])
            print(len(lines))
        x = [x for x in zip(*lines)]
        plot.plot(x[1],x[0],label = 'Operating Line #'+str(len(self.operating_lines)))
        plot.legend()
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

distillate_fraction = 0.7
bottoms_fraction = 0.02
feed = [300,200,200]
feed_composition = [0.4,0.3,0.2]
liquid_composition = [5/4,0,0.75]
relfux_ratio = 1
print(xydata[0])
test = MTMethod(xydata[0],xydata[1],distillate_fraction,bottoms_fraction,feed,feed_composition,liquid_composition,relfux_ratio)
test.find_operating_lines()
test.graph_generator()

