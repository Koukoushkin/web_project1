class NewsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             buy INTEGER(1000)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, buy):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (title, content, buy) 
                          VALUES (?,?,?)''', (title, content, buy))
        cursor.close()
        self.connection.commit()

    def get(self, new_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT buy FROM news WHERE id = ?", (str(new_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def update(self, count, new_id):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE news SET buy = ? WHERE id = ?", (count, str(new_id)))

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id)))
        cursor.close()
        self.connection.commit()
