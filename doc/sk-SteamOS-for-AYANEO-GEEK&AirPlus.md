# SteamOS-for-AYANEO&GEEK&AirPlus

## 镜像发布

下载链接:https://pan.baidu.com/s/1W2jIySkrEuqlpixlZ00rtA?pwd=aabb

### 1.4

- 更新 jupiter-hw-support ，解决插内存卡启动时，容易长时间卡在引导的问题
- 内置了 sk SteamOS 配置工具
- 修正了一些问题

#### 更新方式

1.4 默认只提供root分区镜像，需要从1.3升级。使用DiskGenius还原分区镜像到root分区即可。如果有设置挂载共享分区的，需要重新设置


### 1.3

- 使⽤stable源构建镜像，或许兼容性好⼀点
- 安装少量必要应⽤
- 安装decky插件平台和部分插件
- 安装GE-Proton 8.4
- 默认启⽤HandyGCCS驱动⼿柄按键
- 使⽤dsdt补丁处理 Air Plus 按键驱动问题
- 默认关闭Air Plus 摇杆灯（颜⾊还没法控制）
- 默认为休眠
- 现存问题：GEEK休眠后唤醒触屏会失效
