#coding=utf-8
try: 
  import xml.etree.cElementTree as ET 
except ImportError: 
  import xml.etree.ElementTree as ET 
import sys 

import os
log = "UpdateCbrHash.log"

if os.path.exists(log):
    os.remove(log)

import MySQLdb

def get_node(node_name): 
	for node in root.findall(node_name):
	  node = str(node.text) 
	  print node_name, " : ", node
	  return node


try: 
  tree = ET.parse("UpdateCbrHashConfig.xml")     #打开xml文档 
  root = tree.getroot()         #获得root节点  
except Exception, e: 
  print "Error:cannot parse file:UpdateCbrHashConfig.xml."
  sys.exit(1) 

 
print "*"*10
db_user=get_node("db_user")
db_password=get_node("db_password")
db_ip=get_node("db_ip")
db_name=get_node("db_name")
xml_name=get_node("xml_name")
print "*"*10,"\n\n"

# 打开数据库连接
db = MySQLdb.connect(db_ip,db_user,db_password,db_name)
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
try: 
  tree = ET.parse(xml_name)     #打开xml文档 
  root = tree.getroot()         #获得root节点  
except Exception, e: 
  print "Error:cannot parse file:",xml_name,"."
  sys.exit(1) 
  
print "*"*10
bindings = root.find("Bindings")
for bingding in bindings.findall('Binding'):
  key_id = bingding.find("ProductKeyID").text
  cursor.execute('select hash from product_key where key_id=%s', key_id)
  hash = str(cursor.fetchone())
  hash = hash[2:-3]
  print str(hash)
  st = bingding.find("HardwareHash")
  st.text=str(hash)

# 关闭数据库连接
db.close()

print "*"*10
tree.write(xml_name)

print "pass"


