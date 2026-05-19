from database.DB_connect import DBConnect
from model.arco import Arco
from model.artista import Artista
from model.genere import Genere


class DAO():
    @staticmethod
    def allGenre():
        conn= DBConnect.get_connection()
        cursor= conn.cursor(dictionary=True)
        result=[]
        query=""" select *
                    from genre g """
        cursor.execute(query)
        for row in cursor:
            result.append(Genere(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def allArtist():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """select * 
                    from artist a """
        cursor.execute(query)
        for row in cursor:
            result.append(Artista(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def allNodes(gID):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ select distinct a.ArtistId 
                    from track t , album a 
                    where t.AlbumId =a.AlbumId 
                    and t.GenreId = %s  """
        cursor.execute(query,(gID,))
        for row in cursor:
            result.append(row["ArtistId"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def edgesWPeso(gId):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ SELECT 
                clienti1.ArtistId AS id1, 
                clienti2.ArtistId AS id2, 
                pop1.n1, 
                pop2.n2
            FROM 
                (SELECT DISTINCT a1.ArtistId, i1.CustomerId
                 FROM album a1, track t1, invoice i1, invoiceline i11 
                 WHERE a1.AlbumId = t1.AlbumId 
                   AND t1.TrackId = i11.TrackId 
                   AND i11.InvoiceId = i1.InvoiceId
                   AND t1.GenreId = %s) clienti1 
            JOIN 
                (SELECT DISTINCT a2.ArtistId, i2.CustomerId
                 FROM album a2, track t2, invoice i2, invoiceline i22 
                 WHERE a2.AlbumId = t2.AlbumId 
                   AND t2.TrackId = i22.TrackId 
                   AND i22.InvoiceId = i2.InvoiceId
                   AND t2.GenreId = %s) clienti2 
                ON clienti1.CustomerId = clienti2.CustomerId AND clienti1.ArtistId < clienti2.ArtistId
            JOIN
                (SELECT a1.ArtistId, COUNT(*) AS n1
                 FROM album a1, track t1, invoiceline i11 
                 WHERE a1.AlbumId = t1.AlbumId AND t1.TrackId = i11.TrackId 
                   AND t1.GenreId = %s
                 GROUP BY a1.ArtistId) pop1 
                ON clienti1.ArtistId = pop1.ArtistId
            JOIN
                (SELECT a2.ArtistId, COUNT(*) AS n2
                 FROM album a2, track t2, invoiceline i22 
                 WHERE a2.AlbumId = t2.AlbumId AND t2.TrackId = i22.TrackId 
                   AND t2.GenreId = %s
                 GROUP BY a2.ArtistId) pop2 
                ON clienti2.ArtistId = pop2.ArtistId
            GROUP BY clienti1.ArtistId, clienti2.ArtistId, pop1.n1, pop2.n2"""
        cursor.execute(query,(gId, gId, gId, gId))
        for row in cursor:
            result.append(Arco(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPopolarita(gID):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ SELECT DISTINCT a.ArtistId, COUNT(*) as popolarita 
                    FROM Album a, Track t , Invoice i , InvoiceLine il 
                    WHERE a.AlbumId =t.AlbumId 
                    and t.TrackId =il.TrackId 
                    and il.InvoiceId  =i.InvoiceId 
                    and t.GenreId = %s
                    GROUP BY a.ArtistId  """
        cursor.execute(query,(gID,))
        for row in cursor:
            result.append((row["ArtistId"],
                          row["popolarita"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtist(gID):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ SELECT t1.ArtistID as artistId1, t2.ArtistId as artistId2
                    FROM (SELECT a.ArtistId , i.CustomerId 
                            FROM Album a ,Track t ,Invoice i ,InvoiceLine il 
                            WHERE a.AlbumId =t.AlbumId 
                            and t.TrackId =il.TrackId 
                            and il.InvoiceId  =i.InvoiceId 
                            and t.GenreId =%s
                            GROUP by a.ArtistId, i.CustomerId ) t1,
                            (SELECT a2.ArtistId , i2.CustomerId 
                            FROM Album a2 ,Track t2 ,Invoice i2 ,InvoiceLine il2 
                            WHERE a2.AlbumId =t2.AlbumId 
                            and t2.TrackId =il2.TrackId 
                            and il2.InvoiceId  =i2.InvoiceId 
                            and t2.GenreId =%s
                            GROUP by a2.ArtistId, i2.CustomerId ) t2
                    WHERE  t1.CustomerId=t2.CustomerId
                    and t1.ArtistId<t2.ArtistId
                    group by t1.ArtistId, t2.ArtistId """
        cursor.execute(query, (gID,gID))
        for row in cursor:
            result.append((row["artistId1"],
                           row["artistId2"]))
        cursor.close()
        conn.close()
        return result