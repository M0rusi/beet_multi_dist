## 简介

beet插件，提供配置化的多分发版构建机制。
本插件不会改变beet的默认构建行为


## 功能

1. 同时构建多个分发版
2. 支持模板化的分发版名称
3. 允许自定义分发版构建路径

## 安装
推荐方式：使用python包管理器安装

示例：

```bash
# pip
pip install "multi-dist @ git+https://github.com/M0rusi/beet_multi_dist.git@v0.1.0"
```

```bash
# poetry
poetry add "git+https://github.com/M0rusi/beet_multi_dist.git@v0.1.0"
```

```bash
# uv
uv pip install "multi-dist @ git+https://github.com/M0rusi/beet_multi_dist.git@v0.1.0"
```


## 使用
通过上述任意一种方式安装后，在beet配置文件中启用。

示例：
```yaml
name: example
version: 1.0.0

output: builds
require:
    - multi_dist

meta:
    multi_dist:
        dist_1:                     # 分发版文件/目录的名称
            directory: Releases     # str: 输出文件夹，此项未配置时尝试回退到 beet 输出目录，如果均未配置，该分发版将被跳过
            zipped: true            # bool: 是否打包为zip，默认值为 false
            compression: deflate    # Literal['none'|'deflate'|'bzip2'|'lzma']: 压缩算法。仅 zipped 为 true 时有效。
                                    # 配置为 none 表示不压缩。大小写敏感
            compression_level: 1    # int: 压缩级别。仅 zipped 为 true 时有效。有效值范围由压缩算法决定
            overwrite: true         # bool: 是否覆写。出于数据安全考虑，默认值为 false
            # 如果将此项更改为true，当输出冲突时，beet会删除冲突的文件/目录
            # 在zipped为true时，这会导致同名文件被删除。在zipped为false时，会导致整个目录被删除。
        # 此项最终会生成 `Releases/dist_1.zip` 文件

        dist_2:                        # 支持同时配置多个分发版，各分发版配置项相互独立
            directory: "builds/dist"  # 支持嵌套路径，路径从项目根目录（beet.yml所在目录）算起
            overwrite: true
        # 此项最终会生成 `builds/dist/dist_2` 目录

        "{{ project_name }}_{{ project_version }}_portable":  # 支持模板渲染，渲染上下文为 beet 标准上下文
            zipped: true
        # 此项最终会生成 `builds/example_1.0.0_portable.zip` 文件

# 插件不改变beet的默认行为，由于上述示例中配置了output字段，beet本身会额外生成一份分发版
# 因此使用上述文件会创建总计四份分发版
# 如果希望分发版控制全部由插件处理，不填写output字段即可
# 再次提醒：当output字段不存在时，directory为必填字段
```

## 已知限制
- 不支持将额外构建的分发版链接到存档


## 许可证

本项目以 [MIT](LICENSE) 许可证发布，Copyright (c) 2026 morusi。
使用的第三方组件及其归属声明见 [NOTICE.md](NOTICE.md)。
