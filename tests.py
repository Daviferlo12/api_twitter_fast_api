from db.con import db_client

result = db_client.local.tweets.find({ "by.username": { "$regex": 'strin', "$options" : 'i' } })


for i in result:
    print(i)