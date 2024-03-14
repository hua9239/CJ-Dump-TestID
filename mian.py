import requests

TARGET_URL = "https://cloud.judge.com.tw/course/**/exam/****/problem/"  # + testID
COOKIE_FILE = "cookie.txt"
RESULT_FILE = "result.txt"
TEST_RANGE = [5000, 5601]


def read_cookies(cookie_file):  # 讀取並返回 cookies
    with open(cookie_file, "r", encoding='utf-8') as f:
        xsrf_token = f.readline().strip()
        laravel_session = f.readline().strip()
    return {"XSRF-TOKEN": xsrf_token, "laravel_session": laravel_session}


def check_cookies(cookies):  # 檢查 cookies 是否有效
    response = requests.get(TARGET_URL + "5000", cookies=cookies)
    if "登入" in response.text:
        print("Cookies are invalid.")
        exit()


def read_end_test_id(result_file):  # 讀取結果檔案中最後一筆測試ID
    try:
        with open(result_file, "r", encoding='utf-8') as f:
            lines = f.readlines()
            TEST_RANGE[0] = int(lines[-1].split(",")[0]) + 1
    except (FileNotFoundError, IndexError):
        pass


def fetch_test_titles(target_url, cookies, test_range, result_file):  # 爬取測試標題並寫入到結果檔案中
    for test_id in range(test_range[0], test_range[1]):
        print(f"testID: {test_id:6d}", end="\r")

        response = requests.get(target_url + str(test_id), cookies=cookies)

        if response.status_code != 200:
            continue

        response.encoding = 'utf-8'
        response_text = response.text

        title_start = response_text.find("<font class=\"title_font\">")
        if title_start == -1:
            continue

        title_end = response_text.find("</font>", title_start)
        title = response_text[title_start:title_end]
        title = title[title.find(" - ") + 3:].strip()

        with open(result_file, "a", encoding='utf-8') as f:
            f.write(f"{test_id:4d}, {title}\n")


if __name__ == "__main__":
    cookies = read_cookies(COOKIE_FILE)
    check_cookies(cookies)
    read_end_test_id(RESULT_FILE)
    fetch_test_titles(TARGET_URL, cookies, TEST_RANGE, RESULT_FILE)
