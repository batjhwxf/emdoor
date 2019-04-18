#coding=utf-8
try: 
  import xml.etree.cElementTree as ET 
except ImportError: 
  import xml.etree.ElementTree as ET 
import sys 

import os
log = "SetKeyStatusTo3.log"

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

def set_status_3(po_number):
    try:
        update_status = "update [dbo].[ProductKeyInfo] set [ProductKeyStateID] = 3 where [ProductKeyStateID]=15 and [OEMPONumber]='%s';" %(po_number)
        cur.execute(update_status)
        conn.commit()
    except Exception, e:
        print("Update data error")
        print_error(str(e))


def get_node(node_name): 
    for node in root.findall(node_name):
      node = str(node.text) 
      #print node_name, " : ", node
      return node

if __name__ == "__main__":
    po_number = "ffffff"
    with open('ponumber.txt', 'r') as f:
        po_number = f.read()
    try: 
      tree = ET.parse("SetKeyStatusToConfig.xml")     #打开xml文档 
      root = tree.getroot()         #获得root节点
    except Exception, e:
      print("SetKeyStatusToConfig error")
      print_error(str(e))


    print "*"*50
    db_user=get_node("db_user")
    db_password=get_node("db_password")
    db_ip=get_node("db_ip")
    db_name=get_node("db_name")
    print "*"*50,"\n\n"

    try:
        conn=pymssql.connect(host=db_ip,user=db_user,password=db_password,database=db_name)
        cur=conn.cursor()
        set_status_3(po_number)
        conn.close()
    except Exception, e:
        print_error(str(e))

    f=file(log, "w")
    f.write("pass")
    f.close()

    print_pass()


