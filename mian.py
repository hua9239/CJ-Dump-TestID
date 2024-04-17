import requests
import json

config = json.load(open("config.json", "r", encoding='utf-8'))
email = config["email"]
password = config["password"]
classID = config["classID"]
examID = config["examID"]
testRange = [config["testRange"]["start"], config["testRange"]["end"]]


TARGET_URL = f"https://cloud.judge.com.tw/course/{classID}/exam/{examID}/problem/"
cookies = {}


def login(email, password):
    global cookies
    # 進入登入頁面 獲取 cookies 和 token
    response = requests.get('https://cloud.judge.com.tw/login')
    response.encoding = 'utf-8'
    cookies = response.cookies.get_dict()
    token = response.text.split('name="_token" value="')[1].split('">')[0]

    # 使⽤ cookies 和 token 發送登入請求
    response = requests.post('https://cloud.judge.com.tw/login', cookies=cookies, data={
        '_token': token,
        'email': email,
        'password': password,
    })
    response.encoding = 'utf-8'

    # 嘗試獲取名字 如果失敗則登入失敗
    try:
        name = response.text.split(
            '</span></font>')[1].split('<span')[0].strip()
        print(f"Login as {name}")

    except:
        print("Login failed.")
        exit()

    # 更新全域變數 cookies
    cookies = response.cookies.get_dict()
    # print(cookies)


def logout():   # 登出
    global cookies
    response = requests.get(
        'https://cloud.judge.com.tw/logout', cookies=cookies)
    print(f"Logout")
    cookies = {}


def readLastID():   # 讀取上次的最後一個測試編號
    global testRange

    try:
        with open("result.txt", "r", encoding='utf-8') as f:
            lines = f.readlines()
            testRange[0] = int(lines[-1].split(",")[0]) + 1
    except (FileNotFoundError, IndexError):
        # 如果 result.txt 不存在或是空的，則維持預設
        pass


def fetchTestTitles():  # 爬取測試標題
    for testID in range(testRange[0], testRange[1]):
        print(f"testID: {testID:6d}", end="\r")

        # 請求目標網頁
        response = requests.get(TARGET_URL + str(testID), cookies=cookies)
        # status_code
        # 200 => OK
        # 302 => 登入失敗
        # 500 => 查無此題

        # 如果請求失敗則略過
        if response.status_code == 302:
            print("Login failed.")
            exit()
        elif response.status_code == 500:
            continue

        # 設定編碼
        response.encoding = 'utf-8'
        responseText = response.text

        # 找尋標題
        titleStart = responseText.find("<font class=\"title_font\">")
        # 如果找不到標題則略過
        if titleStart == -1:
            continue

        titleEnd = responseText.find("</font>", titleStart)
        title = responseText[titleStart:titleEnd]
        title = title[title.find(" - ") + 3:].strip()

        # 寫入 result.txt
        with open("result.txt", "a", encoding='utf-8') as f:
            f.write(f"{testID:4d}, {title}\n")

    print("\ncompleted!")


if __name__ == "__main__":
    login(email, password)  # 登入
    readLastID()        # 讀取上次的最後一個測試編號
    fetchTestTitles()   # 爬取測試標題
    logout()            # 登出
