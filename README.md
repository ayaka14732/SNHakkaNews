# 城乡一线（兴宁客家话新闻节目）

## 简介

城乡一线是兴宁本地的民生新闻栏目，创办于 2008 年 4 月。栏目部始终秉持“关注民生，传递信息”的栏目宗旨，深入群众当中，传递政府的声音，反映百姓的诉求。2017 年，围绕“突出民生栏目的服务功能”丰富节目内容，新开发了食品安全监督岗和市民随手拍板块，既宣传推动了市委市政府倡导的创文创卫工作，又契合了广大市民关注的食品安全和环境卫生的需求，受到了广大群众的喜爱。

作为兴宁的主流媒体，城乡一线不仅主动与梅州民生 820、服务 900 等节目对接，而且还结合微信网络题材，挖掘了兴宁托举哥钟汉辉、爱心护士曾丝妮兄妹救人等感人事迹，用饱含真情和激情的文字赞扬真善美，及时宣传发生在我们身边的好人好事，进一步弘扬了社会的正能量。

城乡一线每年播出新闻千余条，帮助群众解决了一大批涉及道路交通、水利环保、扶贫济困、民事维权等公益民生方面的实际问题，为传递正能量、揭露假恶丑、构建和谐社会作出了重要的贡献。未来城乡一线仍将继续发扬兴宁地方特色，聚焦关系民生的问题，以强烈的社会责任感和使命感，及时准确反映老百姓的心声，为老百姓提供贴心实在的服务，全力打造广大人民群众都喜爱的民生新闻品牌栏目。

# 数据格式

数据包含在两个 CSV 文件 `list.csv` 和 `list-sanitized.csv` 中。

其中，`list.csv` 包含在本仓库制作时网络上可以访问的全部数据，但其中一部分数据有误，无法下载。`list-sanitized.csv` 只包含可下载的。

- `DATE`: 视频日期
- `POST_URL`: 文章链接
- `VIDEO_URL`: 视频链接
- `VIDEO_KEY`: 保存在互联网档案馆的文件名

# 制作方法

## 往期视频

```sh
cd scripts/scraper_old
./download_search_results.sh
python process_search_results.py
./download_posts.sh
python process_posts.py
```

## 最新视频

```sh
cd scripts/scraper
python main.py
```

## 检查列表

```sh
python check.py
grep -v ERROR list.csv > list-sanitized.csv
```
