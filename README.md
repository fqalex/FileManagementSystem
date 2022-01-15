#IT设备信息管理系统
###ITDeviceManagementSystem
######https://github.com/fqalex/ITDeviceManagementSystem

这是一个IT设备信息管理系统
使用python开发
___________________
基于两个github开源项目编写
https://github.com/jinixin/upload-demo
https://github.com/JevenM/HTTP_SERVER

##IT维护台账
IT维护台账包括设备的初始化信息，例如服务器/笔记本/台式机台账记账时间、维护操作、花费成本、基础操作系统、软件、此状态备份文件的保存信息等。
IT维护时间：即此操作时的时间，例如设备采购入账、设备维护、设备维修等信息。
维护操作：初始化/升级/维修/维护/检查/查询/出入库等操作。
类型、品牌、型号、硬件参数、硬件编号、软件参数等为升级后、维护后的状态描述。
费用为本次维护操作花费的费用。
从本台账设计模式为本系统的主要信息，IT基础信息台账为维护信息台账的子集，同时“IT维护信息台账”每次更新后，同步更新“IT基础信息台账”，即“IT基础信息台账”是一个可根据时间查询的“时间序列信息表”。默认为当前时间的信息。通过“IT维护信息台账”可以查询到所有时间序列版本的“IT基础信息台账”表
当计算机进行硬件升级时（例如升级内存、硬盘、CPU、主板等）如果有升级后替换下来的硬件，应作为外设、备件重新记入台账。例如升级换下的内存条、硬盘、主板、显示器
###IT维护信息台账

|编号|维护操作|类型|品牌|型号|硬件参数|硬件编号|软件参数|维护时间|费用|维护人员|使用人员|
|--|--|--|--|--|--|--|--|--|--|--|--|
|--|--|--|--|--|--|--|--|--|--|--|--|
|--|--|--|--|--|--|--|--|--|--|--|--|
|--|--|--|--|--|--|--|--|--|--|--|--|								