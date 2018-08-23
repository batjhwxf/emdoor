#coding=utf-8
#UpdateCbrHash
try: 
  import xml.etree.cElementTree as ET 
except ImportError: 
  import xml.etree.ElementTree as ET

import sys 
import os
import ctypes  

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
	sys.exit(1)

def print_pass():
	set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
	print ''
	print '*'*70
	print ''
	print ' PPPPPPPPPPP          AAA               SSSSSSSSSSSS     SSSSSSSSSSSS    '
	print ' PPPPPPPPPPP         AAAAA              SSSSSSSSSSSS     SSSSSSSSSSSS  '
	print ' PPP     PPP        AAA AAA             SSS              SSS      	  '
	print ' PPP     PPP       AAA   AAA            SSS              SSS            '
	print ' PPPPPPPPPPP      AAA     AAA           SSSSSSSSSSSS     SSSSSSSSSSSS   '
	print ' PPPPPPPPPPP     AAAAAAAAAAAAA          SSSSSSSSSSSS     SSSSSSSSSSSS	'
	print ' PPP            AAAAAAAAAAAAAAA                  SSS              SSS   '
	print ' PPP           AAA           AAA                 SSS              SSS   '
	print ' PPP          AAA             AAA       SSSSSSSSSSSS     SSSSSSSSSSSS   '
	print ' ppp         AAA               AAA      SSSSSSSSSSSS     SSSSSSSSSSSS             '
	print ''
	print '*'*70
	print ''
	reset_color()
	win32api.MessageBox(0, 'PASS', "INFO",0) 
	#exit(0)

import win32api,win32con  



log = "UpdateCbrHash.log"

if os.path.exists(log):
    os.remove(log)

import pymssql

import _mssql
import uuid
import decimal

def get_node(node_name): 
    for node in root.findall(node_name):
        node = str(node.text) 
        return node


try: 
  tree = ET.parse("UpdateCbrHashConfig.xml")     #打开xml文档 
  root = tree.getroot()         #获得root节点  
except Exception, e: 
  print_error('Cannot parse file:UpdateCbrHashConfig.xml.') 

 
print "*"*50
db_user=get_node("db_user")
db_password=get_node("db_password")
db_ip=get_node("db_ip")
db_name=get_node("db_name")
print "*"*50,"\n\n"

def main_func(cbr_name):
    if os.path.exists('Cbr'):
        f= open('Cbr/'+cbr_name+'.txt','r')
        txt = f.read()
        txt = str(txt)
        pos1 = txt.find('<?')
        head = ''
        if pos1 != -1:
            pos2 = txt.find('?>')
            head = txt[pos1:pos2+2]
            txt = txt.replace(head, "")
        xmlns_pos1 = txt.find(' xmlns')
        xmlns_pos2 = txt.find('">')
        xmlns = txt[xmlns_pos1:xmlns_pos2+2]
        txt = txt.replace(xmlns, ">")
        print head, xmlns
        f.close() 
        if not os.path.exists('NewCbr'):
            os.makedirs('NewCbr') 
        xml_name = 'newcbr/'+cbr_name+'.xml'
        f = open( xml_name, 'w' )
        print 'new:'
        print txt
        f.write( txt )   
        f.close()
    else:
        print_error('Cbr folder is not exist.')
     
    print xml_name
        
    try:
        db=pymssql.connect(host=db_ip,user=db_user,password=db_password,database=db_name)
        cursor=db.cursor()
    except Exception, e: 
        print_error(str(e))


    try: 
        tree = ET.parse(xml_name)     #打开xml文档 
        root = tree.getroot()         #获得root节点  
    except Exception, e: 
        print_error("Cannot parse file:"+xml_name+".")
 
    print "*"*10
    bindings = root.find("Bindings")
    for bingding in bindings.findall('Binding'):
        key_id = bingding.find("ProductKeyID").text
        cursor.execute('select [hash] from [dbo].[ProductHash] where [key_id]=%s', key_id)
        hash = str(cursor.fetchone())
        if len(hash) > 2000:
            hash = hash[3:-3]
            print '[',str(hash),']'
            st = bingding.find("HardwareHash")
            st.text=str(hash)
        else:
            print_error('key id:'+str(key_id)+", hash length error! "+str(len(hash)))

    # 关闭数据库连接
    db.close()

    print "*"*10
    tree.write(xml_name)
    
    
    f = open( 'newcbr/'+cbr_name+'.xml', 'r+' )  
    txt = f.read()
    txt = head + str(txt)
    txt = txt.replace('<ComputerBuildReport>', '<ComputerBuildReport'+xmlns)
    f.close()
    f = open( 'newcbr/'+cbr_name+'.txt', 'w' )   
    f.write( txt )
    print 'update hash:'
    print txt
    f.close()
    if os.path.exists('newcbr/'+cbr_name+'.xml'):
        os.remove('newcbr/'+cbr_name+'.xml')
    if os.path.exists('Cbr/'+cbr_name+'.txt'):
        os.remove('Cbr/'+cbr_name+'.txt')
    
def ListFilesToTxt(dir,wildcard,recursion):
    exts = wildcard.split(" ")
    files = os.listdir(dir)
    for name in files:
        if (len(name) <= 4) | (name.find('.txt') < 0): 
          print_error('Cbr file error: '+name)
        fullname=os.path.join(dir,name)
        if(os.path.isdir(fullname) & recursion):
            ListFilesToTxt(fullname,wildcard,recursion)
        else:
            for ext in exts:
                if(name.endswith(ext)):
                    print name

                    main_func(name[:-4])
                    #break
def run():
  dir="cbr"     #文件路径
  wildcard = ".txt"      #要读取的文件类型；
  if not os.listdir('cbr'): 
    print_error('Cbr folder is empty.')
  ListFilesToTxt(dir,wildcard, 1)



run()
print_pass()



