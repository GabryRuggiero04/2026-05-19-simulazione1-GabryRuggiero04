from dataclasses import dataclass


@dataclass
class Genere:
    GenreId: int
    Name: str

    def __eq__(self, other):
        return self.GenreId==other.GenreId

    def __hash__(self):
        return hash( self.GenreId)

    def __str__(self):
        return f"{self.Name}-({self.GenreId})"