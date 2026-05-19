from model.model import Model

myModel=Model()
myModel.buildGraph(1)
nNodes, nEdges = myModel.detailsGraph()
print(nNodes, nEdges)