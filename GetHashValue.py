#coding=utf-8
try: 
  import xml.etree.cElementTree as ET 
except ImportError: 
  import xml.etree.ElementTree as ET 
import sys 

import os
log = "GetHashValue.log"

if os.path.exists(log):
    os.remove(log)

import pymssql
import _mssql
import uuid
import decimal
import ctypes  
import sys
import win32api,win32con  
'''Windows CMD命令行颜色'''

# 句柄号
STD_INPUT_HANDLE = -10  
STD_OUTPUT_HANDLE= -11  
STD_ERROR_HANDLE = -12  

# 前景色
FOREGROUND_BLACK    = 0x0 # 黑
FOREGROUND_BLUE     = 0x01 # 蓝
FOREGROUND_GREEN    = 0x02 # 绿
FOREGROUND_RED      = 0x04  # 红
FOREGROUND_INTENSITY = 0x08 # 加亮

# 背景色
BACKGROUND_BLUE     = 0x10 # 蓝
BACKGROUND_GREEN    = 0x20 # 绿
BACKGROUND_RED      = 0x40  # 红
BACKGROUND_INTENSITY = 0x80 # 加亮

colors = [FOREGROUND_BLUE, # 蓝字
          FOREGROUND_GREEN,# 绿字
          FOREGROUND_RED,  # 红字
          FOREGROUND_BLUE  | FOREGROUND_INTENSITY, # 蓝字(加亮)
          FOREGROUND_GREEN | FOREGROUND_INTENSITY, # 绿字(加亮)
          FOREGROUND_RED   | FOREGROUND_INTENSITY, # 红字(加亮)
          FOREGROUND_RED | FOREGROUND_INTENSITY| BACKGROUND_BLUE | BACKGROUND_INTENSITY] # 红字蓝底
          
texts = ['蓝字',
         '绿字',
         '红字',
         '蓝字(加亮)',
         '绿字(加亮)',
         '红字(加亮)',
         '红字蓝底']
          
# See "http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp" for information on Windows APIs.
  
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)  
      
def set_cmd_color(color, handle=std_out_handle):  
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)  
    return bool  
      
def reset_color():  
    set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)  
     
def print_error(text):
	set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
	print ''
	print '*'*70
	print ''
	print ' FFFFFFFFFFF          AAA               IIIIIII      LLL            	  '
	print ' FFFFFFFFFFF         AAAAA              IIIIIII      LLL         	  '
	print ' FFFF               AAA AAA               III        LLL         	  '
	print ' FFFFFFFFFFF       AAA   AAA              III        LLL              	 '
	print ' FFFFFFFFFFF      AAA     AAA             III        LLL         	'
	print ' FFFF            AAAAAAAAAAAAA            III        LLL            '
	print ' FFFF           AAAAAAAAAAAAAAA           III        LLL            '
	print ' FFFF          AAA           AAA        IIIIIII      LLLLLLLLLLLL          '
	print ' FFFF         AAA             AAA       IIIIIII      LLLLLLLLLLLL            '
	print ''
	print ''
	print 'Error: ',text
	print ''
	print '*'*70
	print ''
	reset_color()
	win32api.MessageBox(0, text, "ERROR",0)  
	exit(1)

def print_pass():
	set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
	print ''
	print '*'*70
	print ''
	print ' PPPPPPPPPPP          AAA               SSSSSSSSSSSS     SSSSSSSSSSSS    '
	print ' PPPPPPPPPPP         AAAAA              SSSSSSSSSSSS     SSSSSSSSSSSS    '
	print ' PPP     PPP        AAA AAA             SSS              SSS             '
	print ' PPP     PPP       AAA   AAA            SSS              SSS             '
	print ' PPPPPPPPPPP      AAA     AAA           SSSSSSSSSSSS     SSSSSSSSSSSS    '
	print ' PPPPPPPPPPP     AAAAAAAAAAAAA          SSSSSSSSSSSS     SSSSSSSSSSSS    '
	print ' PPP            AAAAAAAAAAAAAAA                  SSS              SSS    '
	print ' PPP           AAA           AAA                 SSS              SSS    '
	print ' PPP          AAA             AAA       SSSSSSSSSSSS     SSSSSSSSSSSS    '
	print ' ppp         AAA               AAA      SSSSSSSSSSSS     SSSSSSSSSSSS    '
	print ''
	print '*'*70
	print ''
	reset_color()
	win32api.MessageBox(0, 'PASS', "INFO",0) 
	exit(0)

def create_table():
    try:
        create_tb_cmd='''
        CREATE TABLE IF NOT EXISTS [dbo].[ProductHash]
        ([key_id] VARCHAR(100) NOT NULL,
        [state] VARCHAR(100),
        [hash] VARCHAR(max),
        PRIMARY KEY(id)
        );
        ''' 
        cur.execute(create_tb_cmd)  
    except Exception, e:  
        print 'Not create table.'
    try:
        insert_dt_cmd="INSERT INTO [dbo].[ProductHash] ([KEY_ID], [STATE], [HASH]) VALUES ('%s', '%s', '%s');" %(key_id, key_state, key_hash)
        ret=cur.execute(insert_dt_cmd)  
        cur.execute('select [hash] from [dbo].[ProductHash] where [key_id]=%s', key_id)
        hash = str(cur.fetchone())
        print 'hash:', hash
        if len(hash) > 2000:
            pass
        else:
            print_error('key id:'+str(key_id)+", hash length error! "+str(len(hash)))
        conn.commit()
        cur.close() 
    except Exception, e:  
        print_error(str(e))

def get_node(node_name): 
    for node in root.findall(node_name):
      node = str(node.text) 
      #print node_name, " : ", node
      return node

try: 
  tree = ET.parse("GetHashValueConfig.xml")     #打开xml文档 
  root = tree.getroot()         #获得root节点  
except Exception, e: 
  print_error(str(e))


print "*"*50
db_user=get_node("db_user")
db_password=get_node("db_password")
db_ip=get_node("db_ip")
db_name=get_node("db_name")
xml_name=get_node("xml_name")
print "*"*50,"\n\n"

try: 
  tree = ET.parse(xml_name)     #打开xml文档 
  #root = ET.fromstring(country_string) #从字符串传递xml 
  root = tree.getroot()         #获得root节点  
except Exception, e: 
  print_error(str(e))

  
print "*"*50
for key_id in root.findall('ProductKeyID'):
  key_id = str(key_id.text) 
  print key_id
for key_state in root.findall('ProductKeyState'): 
  key_state = str(key_state.text)    
  print key_state 
for key_hash in root.findall('HardwareHash'):
  key_hash = str(key_hash.text)
  print key_hash 
if len(key_hash) < 2000:
  print_error('key id:'+str(key_id)+", hash length error! "+str(len(hash)))
print "*"*50
 
try:
    conn=pymssql.connect(host=db_ip,user=db_user,password=db_password,database=db_name)
    cur=conn.cursor()
except Exception, e:
    print_error(str(e))

'''
cur.execute('SELECT * FROM [dbo].[KeyState]')
row=cur.fetchone()
while row:
    print("%s"%(row[0]))
    row=cur.fetchone()
'''
create_table()
conn.close()

f=file(log, "w")
f.write("pass")
f.close()

print_pass()


