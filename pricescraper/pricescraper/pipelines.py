from itemadapter import ItemAdapter


class PricescraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Extract just title of the medicine
        text_title = adapter.get('title')
        just_title = text_title.split(',')[0].strip()
        adapter['title'] = just_title

        # Extract numerals from price
        price_euro_tuple = adapter.get('price')
        price_euro = price_euro_tuple.replace('\xa0€', '').strip()
        digits = price_euro.replace(',', '.')
        digit = float(digits)
        adapter['price'] = digit

        return item


import sqlite3

class SaveToSQLitePipeline:

    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS prices(
            id INTEGER PRIMARY KEY,
            title TEXT,
            url TEXT,
            price_euro NUMERIC,
            form TEXT,
            code TEXT,
            company TEXT
        )
        """)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database_name=crawler.settings.get(
                'SQLITE_DATABASE_NAME', 'pricespharm.db')
        )

    def process_item(self, item, spider):
        self.cur.execute("""
        INSERT INTO prices (
           title,  url, price_euro, form, code,
            company
            ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
            item['title'],
            item['url'],
            item['price'],
            item['form'],
            item['code'],
            item['company']
        ))

        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
