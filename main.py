import requests
import json

import util
import util as u
from multiprocessing import Pool
import os

SIDE = 0 # 0: left, 1: right

# todo implement a nice way of getting every lecture avaiable and its size, comparing that to what has been
# downloaded already, and then cleanly download new lecture videos while making sure that both sides are not
# exactly t# todo implement a nice way of getting every lecture avaiable and its size, comparing that to what has been
# downloaded
#
he same video. and that assumes there are 2 sides...


class CourseClass:

    def __init__(self, course_code, course_id, r):
        self.course_code = course_code
        self.course_id = course_id
        self.lecture_list = []
        self.lecture_name_list = []
        self.lecture_ids = []
        self.r = r
        self.lecture_json = self.r.get(u.lecture_list(self.course_id), headers=u.headers).json()['data']



    def get_file_name(self, lid):
        files_list = []
        r = requests.get(u.download_list(lid), stream=True, headers=u.headers)
        data = r.json()['data']['primaryFiles']['files']
        for elems in data:
            if elems['label'] == 'Full':
                files_list.append(elems['fileName'])

        try:
            data = r.json()['data']['secondaryFiles']['files']
            for elems in data:
                if elems['label'] == 'Full':
                    files_list.append(elems['fileName'])
        except:
            pass
        return files_list


    def get_lecture_list(self):
        lecture_name_list = []
        lecture_list = []
        for lectures in self.lecture_json:
            if "lesson" not in lectures.keys():
                ### start of an attempt in getting from groups, however the url is different for downloads
                # so basically het the lesson.lesson.id and request that from https://echo360.net.au/lesson/##id##
                # get the download from that and this could may work...
                 if 'lessons' in lectures.keys():
                    for lesson_in_group in lectures['lessons']:
                        if (lesson_in_group['lesson']['medias'] != []):
                            try:
                                temp = lesson_in_group['lesson']['lesson']['name'] + ' ' + str(
                                    lesson_in_group['lesson']['captureStartedAt'])[0:10] + ("side2" if SIDE else "") + ".mp4"
                            except:
                                temp = lesson_in_group['lesson']['lesson']['name'] + ' ' + str(
                                    lesson_in_group['lesson']['startTimeUTC'])[0:10] + ("side2" if SIDE else "") + ".mp4"
                            try:
                                lid = lesson_in_group['lesson']['medias'][0]['id']
                            except:
                                continue
                            temp = temp.replace("/", "").replace("<", "").replace(">", "").replace("\\", "").replace(
                                "\"", "").replace("|", "").replace("?", "").replace("\n","").replace(":","")
                            if len(temp) > 1:
                                lecture_name_list.append(temp)
                                lecture_list.append(
                                    u.download_file(lid, [lesson_in_group['lesson']['medias'][0]['id']], lesson_in_group['lesson']['lesson']['id']))
                        else:
                            pass
            else:
                if (lectures['lesson']['hasVideo'] == True) and (lectures['lesson']['medias'] != []):
                    try:
                        temp = lectures['lesson']['lesson']['name'] + ' ' + str(lectures['lesson']['captureStartedAt'])[0:10] + ("side2" if SIDE else "") +".mp4"
                    except:
                        temp = lectures['lesson']['lesson']['name'] + ' ' + str(lectures['lesson']['startTimeUTC'])[0:10] + ("side2" if SIDE else "") + ".mp4"
                    try:
                        lid = lectures['lesson']['medias'][0]['id']
                    except:
                        print(lectures, self.course_code)
                        continue
                    temp = temp.replace("/", "").replace("<", "").replace(">", "").replace("\\", "").replace("\"", "").replace("|", "").replace("?","").replace("\n","").replace(":","")
                    if len(temp) > 1:
                        lecture_name_list.append(temp)
                        lecture_list.append(u.download_file(lid, self.get_file_name(lid), lectures['lesson']['lesson']['id']))
                else:
                    pass
        self.lecture_list = lecture_list
        self.lecture_name_list = lecture_name_list


    def create_dir(self):
        if not os.path.exists(self.course_code):
            os.mkdir(self.course_code)


    def get_course_code(self):
        return self.course_code

    def downloader(self, lecture_name, r):
        with open(self.course_code + "/" + lecture_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


    def download_all(self):
        self.create_dir()
        self.get_lecture_list()
        for urls, lecture_name in zip(self.lecture_list, self.lecture_name_list):
            try:
                r = requests.get(urls[SIDE], stream=True, headers=u.headers)
            except:
                continue
            if os.path.isfile(self.course_code + "/" + lecture_name):
                x = os.path.getsize(self.course_code + "/" + lecture_name)
                xx = 0
                if os.path.isfile(self.course_code + "/" + lecture_name + "_disp2"):
                    xx = os.path.getsize(self.course_code + "/" + lecture_name + "_disp2")
                y = int(r.headers.get('content-length', 0))
                if x != y and xx != y:
                    print(lecture_name, "exists")
                    print("downloading screen 2")
                    #os.remove(self.course_code + "/" + lecture_name)
                    self.downloader(lecture_name + '_disp2', r)
                else:
                    print('passing', x, y)
            else:
                print("downloading ", lecture_name)
                self.downloader(lecture_name, r)

    def __repr__(self):
        return (self.course_code)


def multi_execute(object):
    object.download_all()

def get_cookie():
    'Cookie: '
    print("Copy paste the request header from echo360 from the network tab in the dev tools\n(Type help for a how to)\n")
    while True:
        cookie = input()
        if cookie == "help" or cookie == "?":
            print("Open chrome \n Log into echo360 \n click f12 \n go to network tab \n hit refresh \n right click -> copy values -> copy request headers\n")
        if cookie == EOFError or cookie == '' or cookie == "TE: trailers":
            if successful:
                return
            else:
                print("Empty")
                raise BaseException("Nothing provided")
        if 'Cookie: ' in cookie:
            with open('cookie.txt', 'w') as f:
                f.write(cookie.split('Cookie: ')[1])
                successful = True


def main(courses = None):
    if os.path.isfile('cookie.txt') :
        if os.path.getsize('cookie.txt') == 0:
            get_cookie()
        else:
            pass
    else:
        get_cookie()
    util.util()
    courses_list = []
    r = requests.session()
    data = r.get(u.course_list, headers=u.headers).json()['data']
    if courses:
        print("Running for specific courses")
        for things in data[0]['userSections']:
            if things['courseCode'] in courses:
                courses_list.append(CourseClass(things['courseCode'], things['sectionId'], r))
    else:
        for things in data[0]['userSections']:
            courses_list.append(CourseClass(things['courseCode'], things['sectionId'], r))
    print(courses_list)
    with Pool(processes=4) as pool:
        pool.map(multi_execute, courses_list)

if __name__ == '__main__':
    #courses = ['COSC477','ENEL373']
    courses = None
    main(courses)