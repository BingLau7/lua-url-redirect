### 文件配置

|\_\_\_\_conf.d *配置文件目录*  
| |\_\_\_\_redirect.conf *配置文件*  
|\_\_\_\_docker *docker依赖*  
| |\_\_\_\_Dockerfile  
| |\_\_\_\_net *openresty url解析库*  
| | |\_\_\_\_url.lua  
| |\_\_\_\_nginx.conf *nginx.conf配置，build时候加入*  
|\_\_\_\_fabfile.py *部署脚本*  
|\_\_\_\_lua *lua脚本*  
| |\_\_\_\_init.lua *init lua*  
| |\_\_\_\_redirect_third_url.lua *转发第三方链接*  
| |\_\_\_\_whilt_domain.lua *白名单*  
|\_\_\_\_README.md  

### 测试环境

##### 配置
1. 安装docker
2. 安装fabric (python2.7)
3. fab docker_build

##### 运行
4. fab docker_run

### 上线
1. fab -R ol deploy
2. fab -R ol reload_nginx

#### 回滚
3. fab -R ol rollback


### 使用文档

1. 调用链接跳转

- **协议**: HTTP  
- **方法**: GET  
- **URL**: http://link.demo.com/redirect  
- **参数**:  

    ```python
    "url": string, 需要跳转的url
    ```

- **说明**:

1. 过滤范围： demo相关url， referer一致url， 白名单内url  
2. 如果url参数解析错误返回状态码400并返回信息URL param error  
3. 如果属于不受信任的外链返回状态码404并返回信息 Not Found  

- **实例**：

1. 正确实例: http://link.demo.com/redirect?url=http://www.kuaizhan.com  
3. 400实例: http://link.demo.com/redirect?url=://www.kuaizhan.com  
2. 404实例: http://link.demo.com/redirect?url=http://www.kuazha.com  
