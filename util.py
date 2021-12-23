from requests.structures import CaseInsensitiveDict

course_list = "https://echo360.net.au/user/enrollments"
lecture_list = lambda x: "https://echo360.net.au/section/" + x + "/syllabus" # 40c860ba-1e6d-44bc-90ad-802e4a425276
download_list = lambda x: 'https://echo360.net.au/api/ui/library/medias/' + x + '/download-info?' # 6760a76f-561a-414d-b2e5-d85b0fa4a733
download_file = lambda x, y: 'https://echo360.net.au/media/download/' + x + '/hd2.mp4?lessonId=' + y #G_9bb9079d-d4c4-4941-9bdd-4d7a57686127_40c860ba-1e6d-44bc-90ad-802e4a425276_2021-07-19T14:00:00.000_2021-07-19T14:55:00.000

cookie = open('cookie.txt').readline()
headers = CaseInsensitiveDict()
headers["authority"] = "echo360.net.au"
headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"'
headers["sec-ch-ua-mobile"] = "?0"
headers["sec-ch-ua-platform"] = '"Windows"'
headers["upgrade-insecure-requests"] = "1"
headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53"
headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
headers["sec-fetch-site"] = "same-origin"
headers["sec-fetch-mode"] = "navigate"
headers["sec-fetch-user"] = "?1"
headers["sec-fetch-dest"] = "document"
headers["referer"] = "https://echo360.net.au/section/"
headers["accept-language"] = "en-GB,en;q=0.9"
headers["cookie"] = cookie