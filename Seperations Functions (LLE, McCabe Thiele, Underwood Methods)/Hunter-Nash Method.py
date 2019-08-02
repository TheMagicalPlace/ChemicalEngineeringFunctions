from numpy import interp
import matplotlib.pyplot as plt
from numpy import array
from scipy.interpolate import CubicSpline as Sinterp
class HunterNash:

    def __init__(self,raffinate_data,extract_data,feed,feed_composition,solvent_inlet_composition):
        hn_plot = plt.figure()
        for i in range(len(raffinate_data[0])):
            plt.plot([extract_data[1][i],raffinate_data[1][i]],[extract_data[0][i],raffinate_data[0][i]],ls = '--')
        self.extract_composition = [0,0,0]
        self. xydata = [raffinate_data,extract_data]
        self.feed = feed
        self.feed_composition = feed_composition
        self.solvent_composition = solvent_inlet_composition
        plt.plot((self.solvent_composition[0],self.feed_composition[1]),
                 (self.solvent_composition[1],self.feed_composition[0]))


    def constraints(self):
        """calculated the values necessary for Hunter-Nash depending on which set of the
        non-vital variables are given"""
        # TODO setup selection of variable sets
        set_vars = input('Imput avalible data from the following: (Solvent Flow and exiting mass fraction,'
                         'Solvent flow and extract ')

    def case_1(self,solvent_flow,raffinate_composition):
        "finds material ballances, case 1 - known solvent flow and know final raffinate composition"
        self.solvent = solvent_flow
        M = self.feed + solvent_flow # Mixing point mass flow
        mixing_composition = [(x*self.feed+y*self.solvent)/M for x,y in zip(self.feed_composition,self.solvent_composition)]
        self.raffinate_composition = [raffinate_composition,interp(raffinate_composition,self.xydata[-1][0],self.xydata[-1][1]),0]
        self.raffinate_composition[-1] = 1-sum(self.raffinate_composition)
        self.extract_composition[0] = Sinterp([mixing_composition[1],self.raffinate_composition[1]],
                                              [mixing_composition[0],self.raffinate_composition[0]],extrapolate=True)(0)
        self.extract_composition[1] = interp(self.extract_composition[0],self.xydata[0][0],self.xydata[0][1])
        self.extract_composition[2] = 1- sum(self.extract_composition)
        self.extract = M*(mixing_composition[0]-self.raffinate_composition[0])/(self.extract_composition[0]-self.raffinate_composition[0])
        self.raffinate = M - self.extract

        plt.plot([self.extract_composition[1],mixing_composition[1],self.raffinate_composition[1]]
                     ,[self.extract_composition[0],mixing_composition[0],self.raffinate_composition[0]])

    def find_operating_point(self):
        """ finds the operating point used to step off stages by finding the intersection of the
        Feed-Extract and Solvent-Raffninate Lines"""
        feed_extract_line = Sinterp([self.extract_composition[1],self.feed_composition[1]],
                                    [self.extract_composition[0],self.feed_composition[0]],extrapolate=True)
        solvent_raffinate_line = Sinterp([self.solvent_composition[1],self.raffinate_composition[1]],
                                         [self.solvent_composition[0],self.raffinate_composition[0]],extrapolate=True)
        print(feed_extract_line,solvent_raffinate_line)
        x = 0
        while abs(feed_extract_line(x)-solvent_raffinate_line(x)) > 0.001:
            x -= 0.005
        self.operating_point = [x,solvent_raffinate_line(x)]
        plt.plot([x,self.extract_composition[1],self.feed_composition[1]],
                                    [feed_extract_line(x),self.extract_composition[0],self.feed_composition[0]])
        plt.plot([x,self.solvent_composition[1],self.raffinate_composition[1]],
                                         [solvent_raffinate_line(x),self.solvent_composition[0],self.raffinate_composition[0]])


    def find_stages(self):
            extract_solute_composition = self.extract_composition[0]
            extract_carrier_composition = self.extract_composition[1]
            extract = self.xydata[0][0]
            raffinate = self.xydata[1][0]
            stage_raffinate_solute_composition = 1
            while stage_raffinate_solute_composition > self.raffinate_composition[0]:
                stage_raffinate_solute_composition = interp(extract_solute_composition,extract,raffinate)
                stage_raffinate_solvent_composition = interp(stage_raffinate_solute_composition,self.xydata[1][0],self.xydata[1][1])
                operating_line = [[self.operating_point[0],stage_raffinate_solvent_composition],[self.operating_point[1],stage_raffinate_solute_composition]]
                plt.plot([stage_raffinate_solvent_composition, extract_carrier_composition],
                         [stage_raffinate_solute_composition, extract_solute_composition])
                operating_line_extract_intersect = Sinterp(operating_line[0], operating_line[1])(0)
                extract_solute_composition = operating_line_extract_intersect
                extract_carrier_composition = interp(extract_solute_composition,self.xydata[0][0],self.xydata[0][1])
                plt.plot(operating_line[0],operating_line[1])

    def generate_plot(self):
        "generates the parts of the plot not dealt with elsewhere in the class"

        for line in self.xydata:
            if line == self.xydata[-1]:
                [x.reverse() for x in line]
                plt.plot(line[1], line[0])
            else:
                plt.plot(line[1], line[0])


        plt.show()


xy1 = [[0,.1105,.1895,.241,.286,.3155,.3505,.4060,.490],
       [.005,.0067,.0115,.0162,.0225,.0287,.0395,.0640,.132]]
xy2 = [ [0, 0.0502, 0.1105, 0.1890, .2550, .3610, .4495, .5320, .490],
        [.9992,.9482,.8871,.8072,.7392,.6205,.5087,.3790,.132]]

feed = 200
feed_composition = []
utest = HunterNash(xy1,xy2,1000,[0.4,0.6,0],[0,0,1])
utest.case_1(1000,0.01)

utest.find_operating_point()


utest.find_stages()

utest.generate_plot()