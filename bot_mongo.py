import datetime
import pymongo
import pandas as pd
from copy import deepcopy


def connect_collection(str):
  db_client = pymongo.MongoClient("mongodb+srv://andrey:28122011@cluster0.i2aesum.mongodb.net/")
  current_db = db_client['TeleBot']

  return current_db[str]

users = connect_collection('users')
group = connect_collection('group')
# materials = connect_collection('materials')

# Book
# def free_washers():
#   res = []
#   for obj in book.find():
#     time = list(obj['time'].values())
#     if True in time:
#       res.append(obj)
  
#   return res

# def free_time(_washer_id):
#   res = []

#   washer = book.find_one({"_id": _washer_id})
#   for time in washer["time"].keys():
#     if washer["time"][time]:
#       res.append(time)

#   return res

# def change_free_time(_washer_id, time, boolValue):
#   washer = book.find_one({ "_id": _washer_id })

#   new_time_obj = deepcopy(washer["time"])
#   new_time_obj[time] = boolValue

#   book.update_one({ "_id": _washer_id }, { "$set": { "time" : new_time_obj } })


# def change_free_time_by_first(time, boolValue):
#   washers = free_washers()
#   washer_id = 0

#   for washer in washers:
#     if washer['time'][time] != boolValue:
#       change_free_time(washer['_id'], time, boolValue)
#       washer_id = washer['_id']
#       break
  
#   return washer_id


#* Users
def check_key(keys, values):
  if (len(keys) != len(values)):
    return False
  filt = {}
  for i in range(len(keys)):
    filt[keys[i]] = values[i]

  obj = users.find_one(filt)
  if obj:
    return True
  return False 


def give_name_by_id(telegram_id):
  return users.find_one({"id": telegram_id})['name']


def give_subjects_by_id(group_id):
  subjects = connect_collection(str(group_id))
  return subjects.find()['subjects']

def add_info(name, surname, univ, fac, group, group_id, phone, telegram_id):
  filt = {"name": name, "surname": surname, "university": univ, "faculty": fac, "group": group}
  users.update_one(filt, { "$set": { "phone" : phone, "id": telegram_id, "group_id": group_id } } )

# Visits
# def add_string(telegram_id, date, full_name, room, time):
#   visits.insert_one({ "id": telegram_id, "date": date, "full_name": full_name, "room": room, "time": time })

# def del_string(telegram_id, date, time):
#   visits.delete_one({ "id": telegram_id, "date": date, "time": time })

# def fill_doc(low_date = datetime.datetime.now() - datetime.timedelta(days=30), high_date = datetime.datetime.now()):
#   # Get data from MongoDB
#     data = list(visits.find({
#       "date": {"$gte": low_date, "$lte": high_date}
#     }))

#     # Create a Pandas DataFrame from the data
#     df = pd.DataFrame(data)