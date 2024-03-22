# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymssql

class NovelscrapyPipeline:
    def open_spider(self, spider):
        # self.connection = pymssql.connect(
        #     'DRIVER={ODBC Driver 18 for SQL Server};SERVER=192.168.152.133;DATABASE=MacsDB;UID=sa;PWD=5cHC*J6x2B'
        # )
        self.connection = pymssql.connect(
            server='192.168.152.133', user='sa', password='5cHC*J6x2B', database='MacsDB'
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                f"INSERT INTO MacsDB.Novel.tab_novel(novel_name, novel_href, novel_context) "
                f"VALUES (N'{item['novel_name']}', N'{item['novel_href']}', N'{item['novel_context']}')"
            )
            self.connection.commit()
        except pymssql.DatabaseError as e:
            print(f"Error occurred while inserting item into the database: {e}")
            self.connection.rollback()
        return item
