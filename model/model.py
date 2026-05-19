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
        self._graph=nx.DiGraph()
        self._edges=None
        self._popolaritaArtistMap={}




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
        #self.addEdgesV1(genre)
        self.addEdgesV2(genre)
        return self._graph

    def addEdgesV1(self, genre):
        self._edges= DAO.edgesWPeso(genre)
        for e in self._edges:
            if (e.id1 in self._nodes and e.id2 in self._nodes):
                if (e.n1>e.n2 or e.n2==e.n1):
                    self._graph.add_edge(self._AllArtistMap[e.id1], self._AllArtistMap[e.id2], weight=e.n1+e.n2)
                if (e.n1<e.n2 or e.n2==e.n1):
                    self._graph.add_edge(self._AllArtistMap[e.id2], self._AllArtistMap[e.id1], weight=e.n1 + e.n2)

    def addEdgesV2(self, genre):
        self._popArtist = DAO.getPopolarita(genre)
        for t in self._popArtist:
            self._popolaritaArtistMap[t[0]]= t[1]
        tupleArtisti=DAO.getArtist(genre)
        for (a1, a2) in tupleArtisti:
            popArtist1=self._popolaritaArtistMap[a1]
            popArtist2=self._popolaritaArtistMap[a2]
            if popArtist1 > popArtist2 or popArtist2 == popArtist1:
                self._graph.add_edge(self._AllArtistMap[a1], self._AllArtistMap[a2], weight=popArtist1 + popArtist2)
            if popArtist1 < popArtist2 or popArtist2 == popArtist1:
                self._graph.add_edge(self._AllArtistMap[a2], self._AllArtistMap[a1], weight=popArtist1+ popArtist2)

    def detailsGraph(self):
        return len(self._graph.nodes()), len(self._graph.edges())