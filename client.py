# coding=utf-8
import socket
 
def main():
    # 1. 创建套接字
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    # 2. 链接服务器
    serverIP = 'localhost'
    serverPort = 9002
    tcpSocket.connect((serverIP, int(serverPort)))
 
    # 3. 发送下载文件的请求
    fileName = '1.txt'
    tcpSocket.send(fileName.encode("utf-8"))
 
    # 4. 接收文件的数据并且保存到文件中, 假设文件的长度不会超过1024
    recvData = tcpSocket.recv(1024)
    if recvData:
        with open("[new]" + fileName, "wb") as f:
            # 不管在这里是否产生异常，那么with这个语句，一定会保证调用f.close()
            f.write(recvData)
        print("ok")
    else:
        print("error")
 
    # 5. 关闭套接字
    tcpSocket.close()
 
 
if __name__ == "__main__":
    main()