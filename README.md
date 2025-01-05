# 瓦力盒子 (WalleCube) UPS Home Assistant 集成

集成通过订阅官方MQTT服务器实现UPS状态实时获取。

# 获取MQTTT账号

## 抓包获取MQTT用户名和密码。

电脑安装好Wireshark等抓包软件，并开启热点和Wireshark（开启抓包后可以输入mqtt过滤包），然后将UPS配网连接到电脑热点上。一切正常的话你就能获取到对应UPS的MQTT认证信息了。获取到信息后就可以将UPS的网络正常切换到路由器去了。

<a href="wireshark"><img src="https://github.com/xswxm/home-assistant-wallecube/blob/main/wireshark.png?raw=true" width="512" ></a>



# 安装方式

## 使用 HACS 安装

[![打开 Home Assistant 并打开 HACS商店内的存储库。](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=xswxm&repository=[home-assistant-wallecube](https://github.com/xswxm/home-assistant-wallecube)&category=integration)

## 手动安装

将 `custom_components` 下的 `wallecube` 文件夹到 Home Assistant 中的`custom_components` 目录，并手动重启 Home Assistant。

# 设置

[![打开 Home Assistant 并设置新的集成。](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=wallecube)

> [!CAUTION]
> 
> 如果您无法使用上面的按钮，请按照以下步骤操作：
> 
> 1. 导航到 Home Assistant 集成页面（设置 --> 设备和服务）
> 2. 单击右下角的 `+ 添加集成` 按钮
> 3. 搜索 `wallecube`

> [!NOTE]
> 
> 1. 设备IMEI 填写获取到的MQTT用户名
> 2. 设备密钥 填写获取到的MQTT密码


# 拓展衍生

因为集成依赖互联网连接，如果需要本地化，也有很多办法。比如可以将官方mqtt服务器地址本地解析到自己的mqtt服务器，然后再转发给官方服务器，这样就既可以本地化，又可以保留原有的功能。
