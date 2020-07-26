# 声明 java 的包名
namespace java com.test.thrift.bilibili
# 声明 python 的包名
namespace py bilibili.api


struct UserInfo {
    # up主的用户名
    1:string name,
    # up主的 uid
    2:i32 uid,
    # up主粉丝数
    3:i32 fans,
    # up主头像图片的url
    4:string face
}

struct UserDetailedInfo {
    # up主的用户名
    1:string name,
    # up主的 uid
    2:i32 uid,
    # up主的等级
    3:i32 level,
    # up主粉丝数
    4:i32 follower,
    # up主的关注数
    5:i32 follow,
    # 获赞数
    6:i32 likes,
    # 播放数
    7:i32 playAmount,
    # 阅读数
    8:i32 readingAmount,
    # 前三个热门视频，以字典形式存储，内容包括视频链接、视频封面、视频名称
    9:list<map<string, string>> videos,
    # up主头像图片的url
    10:string face,
    # up主七天内的粉丝数据
    11:list<i32> fansData
}

service BilibiliService {
    # 获取粉丝总榜上靠前的up主信息，返回一个列表
    list<UserInfo> getTopUpFans();
    # 获取涨粉数据和掉粉数据，返回有序 uid 列表
    list<UserInfo> getTopIncreasingUp();
    list<UserInfo> getTopDecreasingUp();
    # 根据 uid 查询up主详细信息
    UserDetailedInfo getUpInfo(1:i32 uid);
    # 获取各分区播放量总和信息，返回一个 分区名：总播放量 的字典
    map<string, i32> getSubareaPlayAmount();
    # 获取词云所需数据，返回 标签：权重 的字典
    map<string, double> getWordCloud();
}