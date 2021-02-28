import requests
from datetime import date, datetime
import sqlite3

conn = sqlite3.connect("mydatabase.db")
print('БД ок!')
cursor = conn.cursor()

#настройка сервера и даты
server = 'http://10.53.20.15:8042'
today_raw = date.today()
#today = today_raw.strftime("%Y%m%d")
today = "20210226"


def reverse_date(date):
    '''
    получает строку в формате год месяц день, возвращает строку в формате день
    месяц год
    '''
    if len(date) > 8:
        
        dateofbirth_raw = datetime.strptime(date, "%Y%m%d%H%M%S")
        return dateofbirth_raw.strftime('%d.%m.%Y %H:%M')
    else:
        dateofbirth_raw = datetime.strptime(date, "%Y%m%d")
        return dateofbirth_raw.strftime('%d.%m.%Y')

def create_table():
    # Создание таблицы
    cursor.execute("""CREATE TABLE IF NOT EXISTS list_of_patients
                  (studydate TEXT, name TEXT, birthday TEXT, p_sex TEXT,
                  body_part TEXT, SeriesDescription TEXT, report TEXT)
                   """)
    # Сохраняем изменения
    conn.commit()

def orthanc_connect(server,today):
    data = '{ "Level" : "Instance", "Query" : { "StudyDate" : "'+ today + '" } }'
    r = requests.post(server+'/tools/find', auth = ('orthanc', 'orthanc'), data = data)
    if r.status_code == 200:
        print('Все в норме! Сервер отвечает.')
    else:
        print('Что-то пошло не так! ', r.status_code)
    return r.json()


instanceid = orthanc_connect(server,today)

if len(instanceid) == 0:
    print('исследований нет')
else:
    for i in instanceid:
        url = server+'/instances/'+ i +'/simplified-tags'
        info = requests.get(url, auth = ('orthanc', 'orthanc'))
        p = info.json()
        name = p['PatientName']
        birthday = reverse_date(p['PatientBirthDate'])
        age = p['PatientAge']
        if p['PatientSex'] == 'F':
            p_sex = 'Ж'
        else:
            p_sex = 'M'
        studydate = reverse_date(p['StudyDate']+p['StudyTime'])
        body_part = p["BodyPartExamined"]
        seriesdescription = p['SeriesDescription']
        report = input(name+' '+birthday+' '+ body_part+' Ведите описание:') #вставить в другое место

        user_study = (studydate, name, birthday, p_sex,
                      body_part, seriesdescription, report)

        create_table()

        cursor.execute("""SELECT studydate, name, birthday FROM list_of_patients WHERE
                       (studydate LIKE ? AND name = ? AND birthday = ?);""", ('%'+studydate[0:10]+'%', name, birthday))
        search = cursor.fetchone()

        if search is None:
            cursor.execute("""INSERT INTO list_of_patients VALUES(?,?,?,?,?,?,?);
                       """,user_study)
            conn.commit()

cursor.execute("SELECT * FROM list_of_patients WHERE report = '-'")
all_results = cursor.fetchall()
for row in all_results:
    for c in row:
        print(c, end=" ")
    print('\n')

