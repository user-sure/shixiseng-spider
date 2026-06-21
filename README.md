##实习僧 Python岗位信息采集

##项目简介
本项目用于采集实习僧网站上Python实习生岗位的公开信息，实现从数据抓取、清洗到入库存储的完整流程。

技术栈
- **爬虫**：Requests、BeautifulSoup
- **反爬策略**：User-Agent轮换、请求随机延时
- **数据库**：MySQL、PyMySQL
- **数据清洗**：正则表达式、字符串处理

## 实现功能
- 自动翻页抓取多页Python实习岗位信息
- 提取岗位名称、公司名称、工作城市、薪资、学历要求
- 对薪资格式进行清洗，去除多余空格与特殊字符
- 设计MySQL表结构，将清洗后数据批量存入数据库

## 使用步骤

### 1. 安装依赖
```bash
pip install requests beautifulsoup4 pymysql