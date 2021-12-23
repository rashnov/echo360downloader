import requests
import json
import util as u
from multiprocessing import Pool
import os

# dict_keys(['sectionId', 'sectionName', 'lessonCount', 'courseId', 'courseCode', 'courseName', 'termId'])

class CourseClass:
    def __init__(self, course_code, course_id, r):
        self.course_code = course_code
        self.course_id = course_id
        self.lecture_list = []
        self.lecture_name_list = []
        self.r = r
        self.lecture_json = self.r.get(u.lecture_list(self.course_id), headers=u.headers).json()['data']



    def get_lecture_list(self):
        lecture_name_list = []
        lecture_list = []
        for lectures in self.lecture_json:
            if "lesson" not in lectures.keys():
                # todo: fill in the extraction of videos for a group
                pass
            else:
                if lectures['lesson']['hasVideo'] == True:
                    temp = lectures['lesson']['lesson']['name'] + ' ' + str(lectures['lesson']['lesson']['createdAt'])[0:-14] + "side2.mp4"
                    lid = lectures['lesson']['medias'][0]['id']
                    temp = temp.replace("/", "").replace("<", "").replace(">", "").replace("\\", "").replace("\"", "").replace("|", "").replace("?","")
                    if len(temp) > 1:
                        lecture_name_list.append(temp)
                        lecture_list.append(u.download_file(lid, lectures['lesson']['lesson']['id']))
                else:
                    pass
        self.lecture_list = lecture_list
        self.lecture_name_list = lecture_name_list



    def create_dir(self):
        if not os.path.exists(self.course_code):
            os.mkdir(self.course_code)

    def download_all(self):
        self.create_dir()
        self.get_lecture_list()
        for urls, lecture_name in zip(self.lecture_list, self.lecture_name_list):
            # check if file exists
            if os.path.isfile(self.course_code + "/" + lecture_name) or os.path.isfile(self.course_code + "/" + lecture_name):
                pass
            else:
                r = requests.get(urls, stream=True, headers=u.headers)
                with open(self.course_code + "/" + lecture_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)


def multi_execute(object):
    object.download_all()


def main(multi=False, courses=None):
    courses_list = []
    r = requests.session()
    data = r.get(u.course_list, headers=u.headers).json()['data']
    if courses:
        for things in data[0]['userSections']:
            if things['courseCode'] in courses:
                courses_list.append(CourseClass(things['courseCode'], things['sectionId'], r))
    else:
        for things in data[0]['userSections']:
            courses_list.append(CourseClass(things['courseCode'], things['sectionId'], r))
    if multi:
        with Pool(processes=2) as p:
            p.map(multi_execute, courses_list)
    for item in courses_list:
        item.download_all()

def find_duplicates():
    # get current dir uisng os
    # get all files in dir
    current_dir = str(os.getcwd())
    dups = df(current_dir, recursive=True)
    dups.find_dups()
    dups.get_results()


if __name__ == '__main__':
    main(multi=True)
