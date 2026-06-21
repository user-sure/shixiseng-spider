import requests
import re
import time
import random
import pymysql
conn=pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="123456",
    database="实习僧招聘信息",
    charset="utf8mb4"
)
cursor=conn.cursor()
cursor.execute("truncate table inter_job")
conn.commit()
insert_sql="insert into inter_job(`job_name`,`city`,`company`,`salary`) values (%s,%s,%s,%s)"
base_url="https://www.shixiseng.com/app/interns/search/v2?build_time=1781953906151&page={}&type=intern&keyword=&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%85%A8%E5%9B%BD&internExtend="
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
    "referer":"https://www.shixiseng.com/interns?type=intern&city=%E5%85%A8%E5%9B%BD",
    "accept":"application/json, text/plain, */*"
}
for page in range(1,6):
    url=base_url.format(page)
    print(f"当前请求第{page}页链接：{url}")
    try:
       r=requests.get(url,headers=headers)
       r.encoding = "utf-8"
       r=r.json()

       all_data=r["msg"]["data"]
       for data in all_data:
           name = re.sub(r'&#x[0-9a-fA-F]+;?|[()（）]', "", data["name"]).strip()
           city=data["city"]
           company=data["cname"]
           maxsalary=data["maxsalary"]
           minsalary=data["minsalary"]
           if(maxsalary==0):
               salary="薪资面议"
           else:
               salary=f"{minsalary}~{maxsalary}"
           cursor.execute(insert_sql,(name,city,company,salary))
           time.sleep(random.uniform(3,5))
       conn.commit()
       print(f"第{page}页入库完成 ok\n")
       print("ok")
    except Exception as e:
       print("error",e)
conn.close()