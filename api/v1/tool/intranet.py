from random import randint
from fastapi.exceptions import HTTPException

import requests


def approve_and_get_id_name(login_id: str, login_pw: str) -> tuple[int, str]:
    # return (10, "둘길동")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    headers = {'User-Agent': user_agent,
               'Accept'    : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}

    session = requests.Session()
    session.headers.update(headers)

    url_login_page = 'https://hi.hana.hs.kr/member/login.asp'
    session.get(url_login_page)

    url_login_proc = 'https://hi.hana.hs.kr/proc/login_proc.asp'
    login_data = {'login_id': login_id, 'login_pw': login_pw, 'x': str(randint(10, 99)), 'y': str(randint(10, 99))}
    session.post(url_login_proc, headers={'Referer': url_login_page}, data=login_data)

    url_mypage = 'https://hi.hana.hs.kr/SYSTEM_Member/Member/MyPage/mypage.asp'
    response = session.get(url_mypage, headers={'Referer': 'https://hi.hana.hs.kr/'})

    start_index_id = response.text.find("학번 : ") + len("학번 : ")
    student_id = response.text[start_index_id:start_index_id + 5]

    if student_id.isdigit() is False:
        raise HTTPException(status_code=403, detail='인트라넷 아이디와 비밀번호가 일치하지 않습니다')

    end_index_name = response.text.find(" 님 반갑습니다.")
    student_name = response.text[end_index_name - 3:end_index_name]

    return int(student_id), str(student_name)


if __name__ == '__main__':
    print(type(approve_and_get_id_name('id', 'pw')[0]))
