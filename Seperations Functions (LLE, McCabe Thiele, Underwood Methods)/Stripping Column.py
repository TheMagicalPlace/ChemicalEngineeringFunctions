"""
This class uses the McCabe-Thiele method in order to graphical estimate the number of stages required for a given
distillate purity. For this feed information (flow,composition,vapor percent) is required as well as equilibrium data
for the examined system


"""
from matplotlib import pyplot as plot
from numpy import interp
class MTTRectify:

    def __init__(self,equillibrium_data,feed,feed_composition,liquid_fraction,bottoms_composition,boilup_ratio):
        self.eq_data = equillibrium_data
        self.feed_composition_state = [feed,feed_composition,liquid_fraction]
        self.xyline = [x/100 for x in range(1,101)]
        self.bottoms_composition = bottoms_composition
        self.boilup_ratio = boilup_ratio

    def find_operating_line(self):
        self.feed_line = [self.feed_composition_state[2]/ (self.feed_composition_state[2] - 1) * x / 100
                          - self.feed_composition_state[1] / (self.feed_composition_state[2] - 1) for x in range(1, 101)]

        L = self.feed_composition_state[0]*self.feed_composition_state[2]
        B = L/(self.boilup_ratio+1)
        V = L-B+self.feed_composition_state[0]*(1-self.feed_composition_state[2])
        self.stripping_line = [L/V*(x/100)-(L/V-1)*self.bottoms_composition for x in range(1,101)]
        self.distillate_composition = self.find_intersection(self.xyline,self.feed_line,self.xyline,self.stripping_line)
        self.rectifying_line = [self.distillate_composition[0][1] for x in range(1,101)]

    def find_intersection(self,line1x,line1y,line2x,line2y):
        for i in range(1, 1001):
            i = i / 1000
            cordinate1 = interp(i, line1x, line1y)
            cordinate2 = interp(i, line2x, line2y)
            if abs(cordinate1-cordinate2) < 0.005:
                x = interp(cordinate1, line2y, line2x)
                return [[x,cordinate1]]

    def tray_finder(self):
        # TODO This is the inverse of what it needs to be, change to start from the top plate,
        # make sure to use this for rectifying column
        tray_compositions = [[self.distillate_composition[0][1],self.distillate_composition[0][1]]]  # defining plate 1
        while tray_compositions[-1][1] > self.bottoms_composition:

            tray_compositions.append([interp(tray_compositions[-1][1],self.eq_data[1],self.eq_data[0]),
                                      tray_compositions[-1][1]])
            plot.plot([tray_compositions[-2][0], tray_compositions[-1][0]],
                      [tray_compositions[-1][1], tray_compositions[-1][1]], color='black')

            tray_compositions.append([tray_compositions[-1][0],
                                      interp(tray_compositions[-1][0],self.xyline,self.stripping_line)])
            plot.plot([tray_compositions[-2][0], tray_compositions[-2][0]],
                      [tray_compositions[-1][1], tray_compositions[-2][1]], color='black')


    def __str__(self):
        plot.figure()
        self.find_operating_line()
        self.tray_finder()
        plot.plot(self.eq_data[0],self.eq_data[1])
        plot.plot(self.xyline,self.feed_line)
        plot.plot(self.xyline,self.stripping_line,label = 'Operating Line')
        plot.plot(self.xyline,self.xyline)
        plot.plot(self.xyline,self.rectifying_line)
        plot.axis([0,1,0,1])
        plot.legend()
        plot.show()
        return ' '




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

bottoms_fraction = 0.02
feed = 300
feed_composition = 0.6
liquid_composition = 0.9
boilup = 3
test = MTTRectify(xydata,feed,feed_composition,liquid_composition,bottoms_fraction,boilup)

print(test)