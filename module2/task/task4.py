import pymongo
from bson.objectid import ObjectId

# client = pymongo.MongoClient(host='localhost', port=27017)
client = pymongo.MongoClient('mongodb://localhost:27017')

db = client.test  # 获取 test 数据库
collection = db.students  # 获取 students 集合
# student = {
#     'id': '1160300426',
#     'name': 'rocketeerli',
#     'age': 23,
#     'gender': 'male'
# }
# result = collection.insert_one(student)
# print(result.inserted_id)

# student1 = {
#     'id': '1160300425',
#     'name': 'shan',
#     'age': 23,
#     'gender': 'male'
# }
# student2 = {
#     'id': '1160300427',
#     'name': 'yan',
#     'age': 23,
#     'gender': 'male'
# }
# result = collection.insert_many([student1, student2])
# print(result.inserted_ids)

result = collection.find_one({'name': 'rocketeerli'})
print(type(result))
print(result)

# 使用 bson 进行查询
result = collection.find_one({'_id': ObjectId('5e857a2de3c40606f87f2326')})
print(result)

results = collection.find({'age': 23})
print(f"total count number: {results.count()}")
print(f"total count number: {collection.count_documents({'age': {'$gt': 20}})}")
# 排序
results = results.sort('name', pymongo.ASCENDING).skip(8).limit(7)  # 排序 + 偏移前 8 个 + 限制 7 个内
for res in results:
    print(res['age'])

# 更新
condition = {'name': 'rocketeerli'}
student = collection.find_one(condition)
student['age'] = 26
# result = collection.update(condition, student)
result = collection.update_one(condition, {'$set': student})
print(result)
print(result.matched_count, result.modified_count)  # 获得匹配条数和影响条数

condition = {'age': {'$gt': 21}}
# result = collection.update_one(condition, {'$inc': {'age': 1}})
result = collection.update_many(condition, {'$inc': {'age': 1}})
print(result)
print(result.matched_count, result.modified_count)  # 获得匹配条数和影响条数

# 删除
condition = {'name': 'shan'}
result = collection.delete_one(condition)
print(result)
print(result.deleted_count)
result = collection.delete_many({'age': {'$gt': 23}})
print(result)
print(result.deleted_count)
