# 名称定义 #

Controller: 控制器<br/>
Worker: 被控制的设备<br/>

# 架构设计 #

1. Worker 和 Controller 通过 MQTT 协议连接，Worker 注册到 Controller 时提供自己的 ID。<br/>
2. Controller 通过 Worker 的 ID 确定用于传输数据和指令的 topic。<br/>

# topic 设计 #

1. 用于获取 Worker 数据的 topic：<parent topic>/<worker id>/get<br/>
2. 用于发送指令的 topic：<parent topic>/<worker id>/put<br/>

