# coding=utf-8
import socket

def getFileContent(fileName):
    try:
        with open(fileName, "rb") as f:
            fileContent = f.read()
        return fileContent
    except Exception as ret:
        print("下载的文件%s不存在...." % fileName)
 
 
def main():
    # 1. 创建套接字
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    # 2. 绑定
    tcpSocket.bind(("", 9002))
 
    # 3. 监听套接字改为被动套接字
    tcpSocket.listen(128)
     
    # 4. 等待客户端的到来
    while True:
        clientSocket, clientAddr = tcpSocket.accept()
        print("New connection: %s" % str(clientAddr))
 
        # 5. 接收客户端发送过来的文件下载请求（文件名）
        fileName = clientSocket.recv(1024)
        fileName = fileName.decode("utf-8")
        print("file name: %s" % fileName)
 
        # 6. 获取文件中的数据
        fileContent = getFileContent(fileName)
 
        if fileContent:
            # 7. 发送文件数据给客户端
            clientSocket.send(fileContent)
            print("ok")
        else:
            print("error")
 
        # 8. 关闭套接字
        clientSocket.close()
     
    tcpSocket.close()
 
 
if __name__ == "__main__":
    main()