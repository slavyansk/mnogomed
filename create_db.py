import requests
from datetime import date, datetime
from db import Database

db = Database('my_db.db')

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
        examination = p["BodyPartExamined"] + p['SeriesDescription']
        report = '-'

        user_study = (studydate, name, birthday, p_sex, examination, report)


        db.cur.execute("""SELECT studydate, name, birthday FROM list_of_patients WHERE
                       (studydate LIKE ? AND name = ? AND birthday = ?);""", ('%'+studydate[0:10]+'%', name, birthday))
        search = db.cur.fetchone()

        if search is None:
            db.insert(user_study)

db.cur.execute("SELECT * FROM list_of_patients WHERE report = '-'")
all_results = db.cur.fetchall()
for row in all_results:
    for c in row:
        print(c, end=" ")
    print('\n')

