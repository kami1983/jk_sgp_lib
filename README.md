# jk_sgp_lib 

Make Scrapy easier and more versatile.

## v1.1.8 修正早起版本部分BUG

这组API提供，Items、Pipelines、Spiders 三组类库，用来辅助Scrapy 的上层功能实现，帮助爬虫完成页面的区域校对、帮助Pipeline 对Mysql 的直接输出

## Install 安装

* 安装最新版本：`pip install jk-sgp-lib --upgrade --user`
* 仅安装1.1.8版本：`pip install jk-sgp-lib==1.1.8 --upgrade --user`

## 使用方法

### 创建一个普通的Scrapy 项目

* 可以通过 `scrapy startproject` 创建，这是Scrapy 的相关知识，不了解请自行补充。
* 创建之后大致可以得出如下目录结构：
```
# 仅仅介绍与这个项目使用相关的文件。
scrapy_dir
    /spiders # 爬虫文件存放的目录
    items.py # 数据条目定义文件
    pipelines.py # 输出管道定义文件
    settings.py # 设置文件
```

### 辅助格式化 item 对象类

* 需要 `from jk_sgp_lib.items.CJKSGPItem import CJKSGPItem`
* 之后创建一个你需要的item 对象，CJKSGPItem 本身是 scrapy.Item 的子类，所以可以完成可替代
* 继承这个类会增加3个预定义的保留字段：t_signkey，t_group ，t_status 所有jk_sgp_lib 类都会用这些保留字段做识别做标识，所以尽量不要动。
* def setDbSignKey(self, signkey = '') 设置数据库用的唯一索引标识字段，设置后会被自动MD5
* def setDbStatus(self, tstatus ) 设置数据库库表状态索引列，默认值为1
* def setDbGroup(self, tgroup ) 设置数据库库表分组索引列
* def getJsonStr(self) 获取JSON 字符串，这会序列化本对象
* def getMD5Sign(self, makestr) 获取MD5 标识符号，传入makestr ，对其进行MD5序列化

```
# 举例：创建一个 YourItem
class YourItem(CJKSGPItem):

    # 如下是数据列
    s_month = scrapy.Field()  # 月份
    s_name = scrapy.Field()  # 姓名

```

### 直接将爬取的数据输出到MYSQL
* 如下操作会自动将输出的Item 录入到数据库，如果数据重复进行数据表行update，否则执行insert 语句。
* 修改 `pipelines.py` 添加输出管道对象
* 添加：`from jk_sgp_lib.pipelines.AbsJKSGPPipelineOfMysqlSaver import AbsJKSGPPipelineOfMysqlSaver`
```
class YourPipeline(AbsJKSGPPipelineOfMysqlSaver):
    
    def beforeProcessItem(self, item, spider):
        print('必须实现 beforeProcessItem ，否则报错，可以什么都不做。')

    def afterProcessItem(self, item, spider, count):
        print('必须实现 afterProcessItem ，否则报错，可以什么都不做。')
    
```
* 修改settings.py 配置数据库信息和piplines对象
```

MYSQL_DB_NAME = '数据库名称'
MYSQL_HOST = '数据库主机地址'
MYSQL_PORT = 3306
MYSQL_USER = '数据库用户'
MYSQL_PASSWORD = '数据库密码'

# 定义 YourPipeline 为输出管道，数据库配置好后，会自动建表填充数据，要注意有建表权限。
ITEM_PIPELINES = {
    'cpi_extract.pipelines.YourPipeline': 1000,
}
```

