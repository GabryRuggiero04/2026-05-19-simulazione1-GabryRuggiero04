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
    def edgesWPeso():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ select t1.ArtistId, t2.ArtistId, n1, n2
                    from (select a1.ArtistId, i1.CustomerId, count(*)as n1
                                from album a1 , track t1 ,invoice i1 , invoiceline i11 
                                where a1.AlbumId =t1.AlbumId 
                                and t1.TrackId = i11.TrackId 
                                and i11.InvoiceId =i1.InvoiceId
                                group by  a1.ArtistId, i1.CustomerId ) t1 join 
                                (select a2.ArtistId, i2.CustomerId, count(*)as n2
                                from album a2 , track t2 ,invoice i2 , invoiceline i22 
                                where a2.AlbumId =t2.AlbumId 
                                and t2.TrackId = i22.TrackId 
                                and i22.InvoiceId =i2.InvoiceId
                                group by  a2.ArtistId, i2.CustomerId) t2
                    where t1.ArtistId< t2.ArtistId
                    group by t1.ArtistId, t2.ArtistIds  """
        cursor.execute(query)
        for row in cursor:
            result.append(Arco(**row))
        cursor.close()
        conn.close()
        return result