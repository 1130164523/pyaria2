# pyaria2
基于websocket通信的aria2应用封装库

## 使用方式：
如何安装aria2软件不再赘述，自行百度
### 1.修改配置项，开启RPC远程接口
```
enable-rpc=true
rpc-allow-origin-all=true
rpc-listen-all=true
rpc-secret=usertoken
```
### 2.启动aria2
```
aria2c --conf-path=（本地路径）/aria2.conf -D
```

### 3. 导入文件

```
from aria2.websoket import aria2 
from aria2.utils import format_bytes,format_rate 
```



#### 4.初始化实例

##### 基本应用
```
aria=aria2("127.0.0.1",token="usertoken")
options={
        'dir': '保存路径,
        'out':'保存文件名'
    }
aria.addUri([下载url],options )
```

##### 高级应用
参考示例




