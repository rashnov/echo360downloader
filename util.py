from requests.structures import CaseInsensitiveDict

cookie = ''
headers = CaseInsensitiveDict()
course_list = "https://echo360.net.au/user/enrollments"
lecture_list = lambda x: "https://echo360.net.au/section/" + x + "/syllabus" # 40c860ba-1e6d-44bc-90ad-802e4a425276
download_list = lambda x: 'https://echo360.net.au/api/ui/library/medias/' + x + '/download-info?' # 6760a76f-561a-414d-b2e5-d85b0fa4a733


def download_file(x, y, z):
    url_list = []
    for files in y:
        url_list.append('https://echo360.net.au/media/download/' + x + '/' + files + '?lessonId=' + z)
    return (url_list)

def util():
    global cookie
    global headers
    cookie = open('cookie.txt').readline()
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53"
    headers["cookie"] = cookie
