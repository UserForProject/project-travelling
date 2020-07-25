# 声明 java 的包名
namespace java com.test.thrift.spider
# 声明 python 的包名
namespace py spider.api

# 定义每个景点评价信息的实体（类），使用 struct 关键字
struct SceneryInfo {
    1:string name,
    # tag：用来确定属于必游、必玩、必逛中的哪一个标签
    2:string tag,
    # comments：将评价和对应的评论人数用字典存储
    3:map<string, i32> comments
}

service SpiderService{
    # 获取整体的地图数据，在前端页面需要显示时就进行一次调用，返回一个二层映射：
    # 第一层：县名 -- 含有信息的映射集合
    # 第二层：信息名 -- 信息对应值
    map<string, map<string, i32>> getLocationInfo();

    # 根据区域名称查找其对应景点的信息，返回一个 SceneryInfo 的对象列表
    list<SceneryInfo> searchSceneryInfo(1:string name);
}
