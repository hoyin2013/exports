# 根据给出的sql语句导出Oracle或者mysql的数据为csv或excel文件

## 用法

1. 修改config.py ，给config配置正确的信息
2. 将要提取的sql语句存放到sql文件夹下，编码为utf8，末尾不要加“；”号
3. linux直接执行 `python3 exports.py` , windows 执行 `run.bat`
4. 进入exports文件夹找到提取出来的sql语句

## 参数说明

- db_type = 'oracle'  # 数据源为"oracle"或者是"mysql"
- export_type = 'excel'   # 导出文件类型为"excel" 或者"csv"
- mysql_config   # mysql的连接配置
- oracle_config # 暂未使用
- send_to_email = False  # 是否发送邮件

