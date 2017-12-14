import os


if __name__ == "__main__":

    # os.system("scrapy crawl news.qq -o news.csv")
    os.system("scrapy crawl news.fenghuang -o ./data/fenghuangnews.csv")