# ToyChain

## 结构介绍
- configs保存潜在的所有配置文件，命名格式：``xxxCfg.yaml``
- doc保存相关说明文档
- module包含从其他项目引用的功能
- out相关运行结果的保存目录
- plugins包含其他非开源的或可后续扩展的应用程序目录
- pocs包含poc，格式应与nuclear相同，做到能直接导入
- utils自制通用函数库


## 开发计划
- 2023/03/06-2023/03/14 信息收集框架、设计信息收集类
    - 通用开发
        - [v] 支持插件扩展
        - [v] 支持配置文件加载
        - [ ] 支持多线程
        - [ ] 支持win/linux平台

