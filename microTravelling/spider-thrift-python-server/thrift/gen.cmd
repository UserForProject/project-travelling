@echo off
echo gen Python Thrift program file and Java API
thrift --gen py -out ../ spider.thrift
thrift --gen java -out ../../spider-thrift-server-api/src/main/java spider.thrift