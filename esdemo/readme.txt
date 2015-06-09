1. Prepare Your Ubuntu
(1) Install JDK1.7 
sudo apt-get install openjdk-7-jre-headless

(2) Install pymysql
if using PyMySQL
#$ pip install PyMySQL

2. Install Elastic Search 
(1)  Download & Unpack elastic search. The latest stable version is elasticsearch-1.0.1

(2)  Dive into bin dir, Run ES with 
./elasticsearch

Then you will get a rest service @port 9200

3. Build Your Index
Notes: 
a) ES indexes structural documents in JSON Formats
b) ES indexer supports real time updates
c) ES indexer support REST interfaces

Steps:
(1)  Run ReadNews.py to dump news to json format from mysqlDB. Configure your db host user passwd to connect. Adjust SQL query to control size of  batches.For example "select * from news_item where datetime >xxxx ". After configuration. Run with

python ReadNews.py > OutputJson.dat

(2)  Run PushIndexWithKeywords.py to update ES index.

python PushIndexWithKeywords.py ./OutputJson.dat


(3)  Run QueryIndex.py to check out ES functionality

python QueryIndex.py "China"

python QueryIndex.py "China smartphone"