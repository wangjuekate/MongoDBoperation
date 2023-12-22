#start the mongo data base
mongod --config /usr/local/etc/mongod.conf

db.createCollection("appData2")
#getting json

mongoimport --db <database_name> --collection <collection_name> <path to data.json>/data.json


mongorestore --archive='/Users/jjw6286/Downloads/processingdata/Copy of mongo-gplay-2017-07.bz2'

mongorestore --archive=/Users/jjw6286/Downloads/processingdata/mongo-gplay-2017-04.bz2

--nsFrom='gplay.*' --nsTo='gplay04.*'


mongoexport  --db=gplay --collection=appData --out=/Users/jjw6286/Downloads/mongo-gplay-2017-09.json


mongoimport --db gplay03 --collection gplay07 '/Users/jjw6286/Downloads/processingdata/mongo-gplay-2017-01.json'




#check data base in Mongodb
show dbs
use gplay
db.appData.find({}).limit(1)
db.collection.find().sort({age:-1}).limit(1).explain("executionStats")
db.dropDatabase()

db.appData.find().sort({"appData.minInstalls":-1}).limit(1)
db.appData.find({"appData.minInstalls":{$ne: 50}}).limit(10)


db.genreduplicate.drop()

##

# find appIds that are relevant
db.results.save(db.gplay07.find({"appData.minInstalls":{$gte: 1000}}, {_id: 
1, "appData.minInstalls": 1, "appId": 1, "appData.genreId": 1}).toArray())

db.results.save(db.appData.find({"appData.minInstalls":{$gte: 1000}}, {_id: 
1, "appData.minInstalls": 1, "appId": 1, "appData.genreId": 1}).toArray())


db.results.aggregate(
 [
    { $group: { _id: "$appId", dinstinctGenres: { $addToSet: "$appData.genreId" } } },
   {$project: { count: { $size:"$dinstinctGenres" }}},
   { $match: {"count": {$gt: 1}}},
    { $out: { db: "gplay", coll: "genreduplicate" } }

 ]
)

db.genreduplicate.find().count()

'''224'''

#select before and after time ranges

db.appData.aggregate([
  {
    $lookup: {
        from: "genreduplicate",
        localField: "appId",
        foreignField: "_id",
        as: "matched_docs"
      }
   }
   ,
    { $out: { db: "gplay", coll: "Duplicateddata" } }
])


# 

db.Duplicateddata.find().count




#https://medium.com/fasal-engineering/fetching-data-from-different-collections-via-mongodb-aggregation-operations-with-examples-a273f24bfff0

#sources to get different record immediately

db.copyDatabase("db_to_rename","db_renamed","localhost")
use db_to_rename
db.dropDatabase();   
