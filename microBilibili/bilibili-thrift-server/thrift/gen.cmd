@echo off
echo gen Python Thrift program file and Java API
thrift --gen py -out ../ bilibili_info.thrift
thrift --gen java -out ../../bilibili-thrift-server-api/src/main/java bilibili_info.thrift