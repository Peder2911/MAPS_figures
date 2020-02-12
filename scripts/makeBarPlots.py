
from matplotlib import pyplot as plt
from matplotlib import transforms as trsf 
import matplotlib as mpl
import pandas as pd 
from util import blitTo
from collections import defaultdict
import yaml
import functools
import operator

mpl.rc("axes", grid = True, 
    linewidth= 1.5,
    axisbelow = True
    )
mpl.rc("axes.grid",axis = "x")
mpl.rc("axes.spines",top = False, right = False)
mpl.rc("font",size = 25)

with open("data/priocolors.yaml") as f:
    priocolors = yaml.safe_load(f)

with open("data/questions.yaml") as f:
    questions = yaml.safe_load(f)

with open("data/questionScales.yaml") as f:
    questionScales = yaml.safe_load(f)

colors = defaultdict(lambda: priocolors["gray"])

@blitTo("/tmp/rap.png")
def regionAvgPlot(data,region,variable):
    plt.clf()
    summed = data[["department",variable]].groupby("department").mean().sort_values(variable)

    theseColors = colors.copy()
    theseColors[region] = priocolors["lightblue"]

    #plt.style.use("ggplot")

    
    deptcolors = [theseColors[d] for d in summed.index.values]

    fig = plt.gcf()
    fig.set_size_inches(15,10)

    plt.xlim((1,4))

    ax = plt.gca()
    ax.set_xlabel("Satisfacción")
    ax.set_ylabel("Departamento")

    plt.tight_layout()
    plt.subplots_adjust(left = 0.28)

    plt.barh(summed.index,summed[variable],left = 1, color = deptcolors)
    plt.savefig(f"plots/dept/{region}_{variable}.png")

data = pd.read_csv("data/intermediate/fixedScales.csv")
allRegions = set(data.department)
print(allRegions)
for r in allRegions:
    for v in questions["satComponents"]+questions["satContent"]+questions["satPeace"]:
        regionAvgPlot(data,r,v)

regionAvgPlot(data,"Arauca","P35")
