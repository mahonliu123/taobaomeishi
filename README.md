# taobaomeishi

在scrapy的middleware中利用selenium模拟登录淘宝，并且爬取搜索关键词所得到的商品数据，
由于待爬数据是由js渲染生成的，所以带着cookie去请求数据接口，
并用正则匹配出想要的json格式的数据，再解析数据。

由于直接使用selenium来获取cookie会失败，且不带cookie访问数据接口会失败，
所以目前手动复制cookie。

根据爬取的数据，推测cookie过一会会失效，所以目前爬取的数据量不大，项目会不断更新。。。
