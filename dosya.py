import pypyodbc

connection = pypyodbc.connect('DRIVER={SQL Server};SERVER=SAHIN;DATABASE=FilmTabani;UID=sa;PWD=003sahin003')   #PYPYODBC Kütüphanesi ile SQL SERVER BAĞLANTISI SAĞLADIK
tikla = connection.cursor()