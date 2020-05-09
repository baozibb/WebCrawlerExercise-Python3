import pymongo


class Database():
    ''' mongodb 操作 '''
    def __init__(self, options):
        self._mongo_connection_url = options[0][1]
        self._mongo_db_name = options[1][1]
        self._mongo_collection_name = options[2][1]

    def _get_collection(self):
        client = pymongo.MongoClient(self._mongo_connection_url)
        db = client[self._mongo_db_name]
        collection = db[self._mongo_collection_name]
        return collection

    # 保存数据到数据库
    def save_data(self, data):
        collection = self._get_collection()
        collection.update_one({
            'name': data.get('name')
        }, {
            '$set': data
        }, upsert=True)  # 如果不存在，则插入一条数据
