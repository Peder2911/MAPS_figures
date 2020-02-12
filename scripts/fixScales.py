
import numpy as np
import pandas as pd
import string
import yaml
import functools
import operator

with open("data/questions.yaml") as f:
    questions = yaml.safe_load(f)

print(questions)

with open("data/questionScales.yaml") as f:
    questionScales = yaml.safe_load(f)

data = pd.read_csv("data/base_final.csv", encoding = "latin1",low_memory = False)
print(data.P52)

scales = {}
for s in ["scale_satisfaction","scale_goodbad","scale_yesno"]:
    with open(f"data/{s}") as f:
        scales[s.split("_")[1]] = [l.strip() for l in f.readlines()]

# ========================================================
# Transformation functions 

def lookup(x,y):
    """
    Turns a categorical variable into a numerical one, by
    which index it has in Y.
    """
    try:
        return y.index(x)
    except ValueError:
        return np.nan

def nametrans(names):
    """
    Fixes names by fixing spaces and titlecasing them. 
    """
    return [name.replace("_"," ").title() for name in names]

# ========================================================
# Transform categorical variables to scale variables
for collection, variables in questions.items():
    scale = scales[questionScales[collection]]
    for v in variables:
        data[v] = data[v].apply(lookup, y = scale)

data["department"] = nametrans(data.DEPTO)

allQuestions = functools.reduce(operator.add, questions.values())
data.rename({"DEPTO":"department"})
subset = data[["department",*allQuestions]]

print(data.P52)
with open("data/intermediate/fixedScales.csv","w") as f:
    f.write(subset.to_csv())
