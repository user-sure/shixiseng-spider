import requests
import pymysql
import ua_generator
import time
import random
conn=pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='spider_data',
    charset='utf8mb4'
)
cursor=conn.cursor()
cursor.execute("TRUNCATE TABLE aqy_hot_movies")
conn.commit()
insert_sql = """
INSERT INTO aqy_hot_movies (`排名`, `电影名`, `发布日期`, `演员`, `热度`)
VALUES (%s, %s, %s, %s, %s)
"""
url="https://mesh.if.iqiyi.com/portal/lw/v7/channel/film?uid=0&vip=0&auth=&device=4cc1c286ee49096862b0520fc116b044&scale=200&brightness=dark&pcv=17.062.25542&v=17.062.25542&width=933&mode=page&page=1&ad=%5B%7B%22lm%22%3A5%2C%22position%22%3A%22card%22%7D%2C%7B%22position%22%3A%22focus%22%7D%2C%7B%22position%22%3A%22banner%22%7D%2C%7B%22position%22%3A%22theater%22%7D%2C%7B%22lm%22%3A1%2C%22position%22%3A%22video%22%7D%2C%7B%22position%22%3A%22pic%22%7D%2C%7B%22position%22%3A%22screen%22%7D%2C%7B%22position%22%3A%22bannerCard%22%7D%5D&adExt=%7B%22r%22%3A%222.18.0-ares6-pure%22%7D&conduit_id=PPStream&isLowPerformPC=0&os=10.0&osShortName=win10&themeIds=&xcardParam=&numOfRes=0&from=webapp&agenttype=1&platformcode=b6c13e26323c537d&adnToken=%7B%226%22%3A%7B%2211%22%3A%225%3Athird_id%3D58d98afff026621c48697d5cb8a90735%26yyb_open_user_id%3D41abbdabc9df0514cbc45ed3399be3bbe48abb15%22%7D%7D"
ua_obj = ua_generator.generate(device="desktop", browser="chrome")
headers = {
    "User-Agent": ua_obj.text,
    "sec-ch-ua": ua_obj.ch_ua,
    "sec-ch-ua-platform": ua_obj.ch_ua_platform,
    "sec-ch-ua-mobile": ua_obj.ch_ua_mobile
}
print(headers)
r=requests.get(url,headers=headers)
r=r.json()
all_movie=r["items"][2]
movies=all_movie["video"][0]
hot_movie=movies["data"]
rank=0
for movie in hot_movie:
    rank=rank+1           #排名
    name=movie["display_name"] #电影名
    hot_score=movie["hot_score"] #热度
    date=movie["date"]
    year=date["year"]             #发布年份
    contributor_list = movie.get("contributor", [])
    top2_actor = contributor_list[:2]
    actors = "、".join(person["name"] for person in top2_actor)  #两位演员
    cursor.execute(insert_sql,(rank,name,year,actors,hot_score))
    print(f"{rank}  {name}  {year}  {actors}  {hot_score}")
    time.sleep(random.uniform(1,2))
conn.commit()
conn.close()
cursor.close()
print("all_over")
