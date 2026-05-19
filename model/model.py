import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allGenres=None
        self._AllArtist=DAO.allArtist()
        self._AllArtistMap={}
        for a in self._AllArtist:
            self._AllArtistMap[a.ArtistId]= a
        self._nodes =None
        self._graph=nx.DiGraph
        self._edges=None


    def getAllGenre(self):
        self._allGenres= DAO.allGenre()
        return self._allGenres

    def buildGraph(self, genre):
        self._graph.clear()
        self._nodes=DAO.allNodes(genre)
        for n in self._nodes:
            nodoToAdd=self._AllArtistMap[n]
            self._graph.add_node(nodoToAdd)
        #archi
        self.addEdges()
        return self._graph

    def addEdges(self):
        self._edges= DAO.edgesWPeso()
        for e in self._edges:
            if (e.n1!=e.n2):
                if (e.n1>e.n2):
                    self._graph.add_edge(e.ArtistId1, e.ArtistId2, weight=e.n1+e.n2)
                else:
                    self._graph.add_edge(e.ArtistId1, e.ArtistId2, weight=e.n1 + e.n2)
            else:
                self._graph.add_edge(e.ArtistId1, e.ArtistId2, weight=e.n1 + e.n2)
                self._graph.add_edge(e.ArtistId1, e.ArtistId2, weight=e.n1 + e.n2)


    def detailsGraph(self):
        return len(self._graph.nodes()), len(self._graph.edges())