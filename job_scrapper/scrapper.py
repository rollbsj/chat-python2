from html import escape
import requests
from bs4 import BeautifulSoup


job_list = [] # job_list 초기화는 전역으로 이동
def search_incruit(keyword, num_pages=1): # page 인자 이름 변경, 기본값 1
    for i in range(num_pages): # num_pages 만큼 반복
        # incruit 페이지네이션은 no={페이지 번호} 형태로 가정합니다.
        # 한 페이지당 30개 항목이 있다고 가정하고 offset을 계산합니다.
        page = i * 30
        response = requests.get(f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}&starno={page}")
        # print(f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}&no={page_offset}")
        # print(response.text)

        soup = BeautifulSoup(response.text, "html.parser")

        lis=soup.find_all("li", class_="c_col")

        if not lis: # 더 이상 공고가 없으면 반복 중단
            break

        for li in lis:
            company=li.find("a", class_="cpname").text
            title=li.find("div",class_="cl_top").find("a").text
            location = li.find("div",class_="cl_md").find_all("span")[0].text
            link = li.find("div", class_="cl_top").find("a").get("href")

            job_data = {
                    "회사이름": company,
                    "공고제목" : title,
                    "회사장소": location,
                    "자세히보기": link
                }

            job_list.append(job_data) # 들여쓰기 수정

    # 🔹 전체 출력
    print(f"총 {len(job_list)}개 공고 수집")
    for job in job_list:
        print(job)

    return job_list

job_list = search_incruit("파이썬",3) # num_pages 인자 추가

import csv  

with open("jobs.csv","w",newline="",encoding="cp949") as file:
    writer = csv.writer(file)

    writer.writerow(["회사이름", "공고제목", "회사장소", "자세히보기"])

    for job in job_list:
        writer.writerow([job["회사이름"],job["공고제목"],job["회사장소"],job["자세히보기"]])
        