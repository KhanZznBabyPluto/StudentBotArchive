import numpy as np
import pandas as pd

students_db = pd.read_csv('data/Students.csv')
archive_db = pd.read_csv('data/Archiv.csv')

def check_id(id):
    return id in students_db["Telegram id"].tolist()

def check_name(name):
    return name in students_db["name"].tolist()

def check_surname(name, surname):
    pass