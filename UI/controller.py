from logging import disable

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genreValue= None
        self._artistValue= None

    def fillDDGenre(self):
        allGenres= self._model.getAllGenre()
        for g in allGenres:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(data=g,
                                    text=g.Name,
                                    on_click= self.choiseGenre))
    def choiseGenre(self, e):
        self._genreValue=e.control.data
        return self._genreValue

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        if self._view._ddGenre.value==None:
            self._view.create_alert("Scegliere un genere")
            return
        grafo=self._model.buildGraph(self._genreValue.GenreId)
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )
        numNodes, numEdges= self._model.detailsGraph()
        self._view.txt_result.controls.append(
            ft.Text(f"Numero nodi: {numNodes}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero archi: {numEdges}")
        )
        #influenza artista
        nodeBest, infBest=self._model.influenzaNode()
        self._view.txt_result.controls.append(
            ft.Text(f"Artista più influente: {nodeBest.Name}, con influenza: {infBest}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Top 5 archi:")
        )
        edges= list(grafo.edges(data=True))
        edges.sort(key=lambda e: e[2]['weight'], reverse=True)
        for e in edges[:5]:
            self._view.txt_result.controls.append(
                ft.Text(f"{e[0].Name} -->{e[1].Name}: {e[2]['weight']}")
            )
        self._view._ddArtist.disabled=False
        self._view._btnTrovaCammino.disabled = False
        self.fillDDArtist()
        self._view.update_page()

    def fillDDArtist(self):
        artistGraph= self._model.getAllArtistGraph()
        for a in artistGraph:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(data=a,
                                   text=a.Name,
                                   on_click=self.choiseArtist))
    def choiseArtist(self, e):
        self._artistValue=e.control.data
        return self._artistValue

    def handleCammino(self,e):
        self._view.txt_result.controls.clear()
        if self._view._ddArtist.value is None:
            self._view.create_alert("Selezionare un artista!!")
            return
        path, lenPath=self._model.getPath(self._artistValue)
        self._view.txt_result.controls.append(
            ft.Text(f"Il cammino più lungo dal/dagli artita/artisti {self._artistValue.Name}"
                    f" con successori con peso crescente è lungo: {lenPath}")
        )
        self._view.txt_result.controls.append(
            ft.Text("Cammino:")
        )
        for n in path:
            self._view.txt_result.controls.append(
                ft.Text(n.Name)
            )
        self._view.update_page()