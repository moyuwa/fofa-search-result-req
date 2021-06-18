# fofa-search-result-req
fofaserach result reptile for not VIP user（fofa搜索结果爬取，非VIP用户）

网站
  不注册只能获取10条数据
  注册用户能提取50条
  会员更多

非api方式调用
会员用户根据代码注释，自行修改page=5限制

如果系统不是gbk编码请修改code = key.decode('gbk') 为code = key.decode('utf-8')

**fofa2.0更换了全部网页元素，脚本已无法使用，可做参考编写2.0的爬虫**

