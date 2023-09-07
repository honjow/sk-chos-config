# SK-ChimeraOS-介绍与更新说明

## 介绍

这是一个基于 ChimeraOS 定制修改分发的系统。同步 ChimeraOS 更新，并进行个人定制修改。

## 特点

- 持续跟进 ChimeraOS 更新，保持最新
- 直接通过 Steam 中的检查更新功能进行更新，不需要重新安装系统

## 安装方式

### DiskGenius 恢复镜像

- 免去在线下载镜像的麻烦，直接使用 DiskGenius 还原镜像到磁盘
- 默认只做单系统镜像，有双系统需求的可以通过分区克隆的方式处理。镜像为 DiskGenius 格式，可以直接使用DiskGenius还原到磁盘或者分区。需要进行分区克隆需要先用 DiskGenius 将 pmfx 磁盘镜像文件转为 vmdk 或者 vhd 格式，然后才克隆
- 通过修改睡眠配置参数，使默认睡眠行为都以休眠来实现，解决一些睡眠bug，同时也能降低功耗。但是缺点就是休眠和恢复的耗时比较长。休眠和睡眠可以通过内置的 SK ChimeraOS  配置工具来切换。
- 预装Decky以及基本的一些插件，开箱即用
- 内置 SK ChimeraOS 工具，可以方便的修改系统配置，安装一些特定插件等。

#### 恢复镜像的特别说明

目前网盘中有两个版本，不带`no-swap-partition`后缀的是带有32G Swap分区的，带有`no-swap-partition`后缀的是Swap分区的。如果已经刷过了带swap分区的版本，使用系统更新正常更新即可，不需要换成不带swap分区的版本。最新系统本身是没有区别的。但是无swap分区版本会自动创建和内存大小一致的swap文件，所以预留空间一定要足够。否则休眠功能将会受到影响。

恢复镜像只分了40G空间，以使用大约10G，只剩下30G左右。这是没法给32G内存设备创建swapfile的。所以恢复镜像后，请在后方预留足够未分配空间。系统启动后会自动扩容处理。

下载链接: [https://pan.baidu.com/s/1W2jIySkrEuqlpixlZ00rtA?pwd=aabb](https://pan.baidu.com/s/1W2jIySkrEuqlpixlZ00rtA?pwd=aabb)

### ISO 安装镜像

适合喜欢原汁原味安装体验的用户，缺点需要在线下载，以及只能全盘安装。安装方式与 ChimeraOS 官方一致。
地址：[https://github.com/honjow/install-media/releases](https://github.com/honjow/install-media/releases)
