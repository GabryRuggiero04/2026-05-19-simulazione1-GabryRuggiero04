import copy

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
    def getAllArtistGraph(self):
        artist=[]
        for n in self._nodes:
            artist.append(self._AllArtistMap[n])
        return artist

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

    def influenzaNode(self):
        infBest=0
        nodeBest=None
        for node in self._graph.nodes():
            sommaUscente = 0
            sommaEntrante = 0
            for node, v, data  in self._graph.out_edges(node, data=True):
                sommaUscente+=data['weight']
            for u, node, data in self._graph.in_edges(node, data=True):
                sommaEntrante+=data['weight']
            if (infBest<sommaUscente-sommaEntrante):
                nodeBest=node
                infBest=sommaUscente-sommaEntrante
        return nodeBest, infBest

    def getPath(self, source):
        parziale=[source]
        self._path=[]
        self._bestLen=0
        self.ricorsione(parziale)
        return self._path, self._bestLen

    def ricorsione(self, parziale):
        lunghezza=len(parziale)
        print(lunghezza)
        if lunghezza>self._bestLen:
            self._bestLen=lunghezza
            self._path=copy.deepcopy(parziale)
        successori=list(self._graph.successors(parziale[-1]))
        if len(successori)==0:
            print(f"   [BLOCCO] {parziale[-1].Name} non ha nessun successore! Torno indietro (pop).")
        for nodeCorrente in successori:
            if nodeCorrente not in parziale:
                if self.condizionePeso(parziale, nodeCorrente):
                    parziale.append(nodeCorrente)
                    self.ricorsione(parziale)
                    parziale.pop()

    def condizionePeso(self, parziale, nodo):
        dati_nuovo = self._graph.get_edge_data(parziale[-1], nodo)
        if dati_nuovo is None: return False
        pesoE = int(dati_nuovo["weight"])  # Mettiamo int() per sicurezza!

        if len(parziale) == 1: return True

        dati_vecchio = self._graph.get_edge_data(parziale[-2], parziale[-1])
        if dati_vecchio is None: return False
        peso_vecchio = int(dati_vecchio["weight"])  # Mettiamo int() per sicurezza!

        # AGGIUNGI QUESTA STAMPA MAGICA
        print(
            f"Tento passaggio: {parziale[-2].Name} -> {parziale[-1].Name} (Peso vecchio: {peso_vecchio}) VS {parziale[-1].Name} -> {nodo.Name} (Peso in analisi: {pesoE})")

        if peso_vecchio > pesoE:
            print("---> ACCETTATO! Salto a lunghezza successiva.")
            return True
        else:
            print("---> RIFIUTATO! Il peso non è crescente.")
            return False


