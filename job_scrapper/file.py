import csv

with open("jobs.csv","w",newline="",encoding="cp949") as file:
    writer = csv.writer(file)

    writer.writerow(["회사이름", "공고제목", "회사장소", "자세히보기"]) # 딕셔너리 대신 리스트 사용, 회사위치 -> 회사장소

    for job in job_list: # jobs 대신 job_list 사용
        writer.writerow([job["회사이름"],job["공고제목"],job["회사장소"],job["자세히보기"]]) # 회사위치 -> 회사장소