import pymongo

user = "root"
pwd = "root"
host = "192.168.1.105"
port = "27017"
client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(user, pwd, host, port))
bilibiliData = client["bilibili"]

if __name__ == "__main__":
    # 设置词云输出文件的位置
    with open("E:\Workspace\IdeaProjects\wordcloud\output\wc\part-r-00000", "rb") as f:
        # 每次更新都删除集合重建，防止插入错误
        bilibiliData["wordCloud"].drop()
        wordCloud = bilibiliData["wordCloud"]
        # 插入文件中的所有词
        lines = f.read().decode("utf8").split("\n")
        for line in lines:
            data = line.split("\t")
            # 防止文件末尾或空行导致错误
            try:
                # 强制转换防止排序出错
                wordCloud.insert_one({"word": data[0].strip(), "heat": float(data[1].strip())})
            except IndexError:
                print("跳过无效行")
