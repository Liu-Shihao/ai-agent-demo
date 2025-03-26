import logging
import os
import sys

import requests
import re
from urllib.parse import urljoin
from readabilipy import simple_json_from_html_string
from markdownify import markdownify as md

logger = logging.getLogger(__name__)

"""
你需要安装 `readabilipy` 这个 Python 库。可以使用 pip 来安装：

```bash
pip install readabilipy markdownify
```

这个库是一个用于从 HTML 内容中提取可读文本的工具，它基于 Mozilla 的 Readability 算法。它可以帮助你：
1. 从网页中提取主要文章内容
2. 移除广告、导航栏等无关内容
3. 提取标题、正文等关键信息

你需要安装 `markdownify` 这个 Python 库。可以使用 pip 来安装：

```bash
pip install markdownify
```

这个库的主要功能是将 HTML 内容转换为 Markdown 格式。在你的代码中，它被用来将文章的 HTML 内容（`html_content`）转换为更易读的 Markdown 格式。
这个转换是通过 `markdownify as md` 这个函数来实现的。
"""


class Article:
    url: str

    def __init__(self, title: str, html_content: str):
        self.title = title
        self.html_content = html_content

    def to_markdown(self, including_title: bool = True) -> str:
        markdown = ""
        if including_title:
            markdown += f"# {self.title}\n\n"
        markdown += md(self.html_content)
        return markdown

    def to_message(self) -> list[dict]:
        image_pattern = r"!\[.*?\]\((.*?)\)"

        content: list[dict[str, str]] = []
        parts = re.split(image_pattern, self.to_markdown())

        for i, part in enumerate(parts):
            if i % 2 == 1:
                image_url = urljoin(self.url, part.strip())
                content.append({"type": "image_url", "image_url": {"url": image_url}})
            else:
                content.append({"type": "text", "text": part.strip()})

        return content


class JinaClient:
    def crawl(self, url: str, return_format: str = "html") -> str:
        headers = {
            "Content-Type": "application/json",
            "X-Return-Format": return_format,
        }
        if os.getenv("JINA_API_KEY"):
            headers["Authorization"] = f"Bearer {os.getenv('JINA_API_KEY')}"
        else:
            logger.warning(
                "Jina API key is not set. Provide your own key to access a higher rate limit. See https://jina.ai/reader for more information."
            )
        data = {"url": url}
        response = requests.post("https://r.jina.ai/", headers=headers, json=data)
        return response.text





class ReadabilityExtractor:
    def extract_article(self, html: str) -> Article:
        article = simple_json_from_html_string(html, use_readability=True)
        return Article(
            title=article.get("title"),
            html_content=article.get("content"),
        )


class Crawler:
    def crawl(self, url: str) -> Article:
        # To help LLMs better understand content, we extract clean
        # articles from HTML, convert them to markdown, and split
        # them into text and image blocks for one single and unified
        # LLM message.
        #
        # Jina is not the best crawler on readability, however it's
        # much easier and free to use.
        #
        # Instead of using Jina's own markdown converter, we'll use
        # our own solution to get better readability results.
        jina_client = JinaClient()
        html = jina_client.crawl(url, return_format="html")
        extractor = ReadabilityExtractor()
        article = extractor.extract_article(html)
        article.url = url
        return article


if __name__ == "__main__":
    """
    这段代码是在处理命令行参数：

```python:/Users/liushihao/Downloads/Projects/langmanus/src/crawler/crawler.py
    if len(sys.argv) == 2:
        url = sys.argv[1]
```

具体解释：
1. `sys.argv` 是一个列表，包含了命令行参数：
   - `sys.argv[0]` 是程序本身的名称
   - `sys.argv[1]` 是第一个命令行参数
   
2. `len(sys.argv) == 2` 检查是否有一个命令行参数（程序名称 + 1个参数 = 2）

3. 如果有参数，就将第一个参数（`sys.argv[1]`）赋值给 `url` 变量

例如，当你在命令行这样运行程序时：
```bash
python crawler.py https://example.com
```
- `sys.argv[0]` 是 "crawler.py"
- `sys.argv[1]` 是 "https://example.com"

这样用户就可以通过命令行指定要爬取的网址。如果没有提供参数，代码会使用默认的 URL（在后面的代码中可以看到默认值是 "https://fintel.io/zh-hant/s/br/nvdc34"）。
    """

    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        url = "https://baike.baidu.com/item/%E6%9D%A8%E5%B9%82/149851"
    crawler = Crawler()
    article = crawler.crawl(url)
    print(article.to_markdown())
    """
    /Users/liushihao/miniconda3/envs/langgraph/bin/python /Users/liushihao/PycharmProjects/ai-agent-demo/src/tool/crawler.py 
Jina API key is not set. Provide your own key to access a higher rate limit. See https://jina.ai/reader for more information.

added 61 packages in 2s

13 packages are looking for funding
  run `npm fund` for details
# 杨幂

大事记
---

播报

编辑

1986年9月12日

### 出生 [478]

1986年9月12日出生于北京，因父母均是杨姓，也就是“杨”的3次方，故而得名为幂。

1990年

### 首次出演电视剧 [478]

1990年，正在参加小演员培训班的杨幂被选入陈家林导演的《唐明皇》剧组，在剧中饰演咸宜公主。

1991年

### 大荧幕首秀 [478]

1991年，参演由周星驰主演的古装动作喜剧片《武状元苏乞儿》。

2005年

### 考入北京电影学院 [469]

2005年，杨幂考入北京电影学院表演系。

2006年

### 崭露头角 [471]

2006年，因饰演金庸武侠剧《神雕侠侣》中的郭襄而崭露头角。

2009年4月

### 入选“四小花旦” [479]

2009年4月，在由百万民众参与，近百名娱乐记者联合票选的“80后新生代娱乐大明星”评选中，杨幂与黄圣依、王珞丹、刘亦菲共同获得了内地新“四小花旦”的称号

2009年

### 凭借《仙剑奇侠传三》被大众熟知 [473] [480]

2009年6月，其主演的《仙剑奇侠传三》全国首播，杨幂在剧中一人分饰夕瑶和雪见两角，并成功通过该剧被大众熟知。

2011年

### 主演的《宫锁心玉》掀起热潮 [474] [481-483]

2011年，其主演的宫斗穿越剧《宫锁心玉》开播，剧播期间收视率屡创新高，杨幂凭借该剧首次登上福布斯中国名人榜，并获得了包括第17届上海电视节“白玉兰“奖“最具人气女演员”在内的多个影视奖项。其演唱的主题曲《爱的供养》亦被广为传唱。

2012年1月4日

### 发行首张个人音乐专辑 [484]

2012年1月4日，发行首张个人音乐专辑《亲幂关系》。

2012年

### 获金鹰最具人气女演员奖 [485]

2012年，杨幂获第9届金鹰节最具人气女演员奖。

2014年

### 结婚生女 [486]

2014年1月8日，杨幂与刘恺威在巴厘岛举办了结婚典礼。同年6月1日，在香港产下女儿小糯米。

2015年

### 自立门户 [487]

2015年，杨幂与两位经纪人赵若尧、曾嘉共同出资300万成立了海宁嘉行天下影视文化有限公司，并于同年签约了一批艺人。

2015年7月

### 主演的系列电影《小时代》宣告完结 [488]

2015年7月，其主演的系列电影《小时代》宣告完结，最终票房成绩超过了18亿人民币，创造了国产系列电影的票房记录。

2017年

### 主演的《三生三世十里桃花》首播 [489]

2017年，领衔主演的电视剧《三生三世十里桃花》上星播出 ，该剧以双台平均破一的成绩取得了全国同时段电视剧收视冠军。

2017年

### 获得首个国际电影节影后 [490]

2017年，凭借《逆时营救》获得了第50届休斯敦国际电影节最佳女主角奖，这也是其演艺生涯中首个国际电影节最佳女主角奖项。

2018年12月22日

### 宣布离婚 [491]

2018年12月22日，杨幂和刘恺威发表声明，宣布已于年内离婚，之后两人会以亲人的身份共同抚养女儿。

2018年12月28日

### 获得中国电视好演员优秀演员奖 & “绿宝石”女演员奖 [492]

2018年12月28日，在“第五届中国电视好演员”评选中获中国电视好演员优秀演员奖和“绿宝石”女演员奖两项荣誉。

2019年12月

### 任中国电影家协会青年和新文艺群体工作委员会副会长 [493]

2019年12月，被任命为中国电影家协会青年和新文艺群体工作委员会副会长。

2020年

### 再次担任多个影视行业相关职务 [494-495]

2020年8月，杨幂被任命为中国广播电视社会组织联合会演员委员会常务理事；同年9月，她还担任了北京电视艺术家协会演员工作委员会副会长。

2021年2月12日

### 首登央视春晚舞台 [496]

2021年2月12日，在中央广播电视总台春节联欢晚会上与刘烨、李沁等人共同表演了歌舞《燃烧的雪花》。

展开全部

早年经历
----

播报

编辑

杨幂

1986年9月12日， [469]杨幂出生在北京市宣武区（已并入新的北京市西城区）的一个民警家庭中。 [5-6]因为一家三口都姓杨，也就是“杨”的3次方（数学中乘方的结果叫做幂），所以给她起名杨幂。 [7]

杨幂是地道的北京南城胡同小妞， [8]小时候的她比较顽皮，杨幂父母按照惯常家长们会采取的教育模式，带着小杨幂去学学钢琴、唱歌、画画，培养一下女儿的业余爱好，但是她却静不下心来学习东西，当时中国儿童电影制片厂召开儿童影视表演培训班，于是父母抱着参与试试的心态带着她去报名，结果年龄不足的杨幂却被招生老师破格录取。 [9-10]此外，杨幂还是个正义感十足的女生，在她的概念里做错事就要被惩罚，朋友被欺负了她一定会一马当先打抱不平，这也让她在邻居、朋友之间获得了“小厉害”的外号。 [10]

杨幂童年照

演艺经历
----

播报

编辑

1990年，杨幂当时参加中国儿童电影制片厂的儿童影视表演培训 [10]，刚好《[唐明皇](/item/%E5%94%90%E6%98%8E%E7%9A%87/7040?fromModule=lemma_inlink)》剧组来挑选小演员，而4岁的杨幂幸运地被挑上了，并出演了剧中的咸宜公主 [9] [478]，该剧则在播出后获得了第11届“[金鹰奖](/item/%E9%87%91%E9%B9%B0%E5%A5%96/1952168?fromModule=lemma_inlink)”优秀长篇连续剧奖、 [498]第13届“[飞天奖](/item/%E9%A3%9E%E5%A4%A9%E5%A5%96/0?fromModule=lemma_inlink)”长篇特等奖 [11]。1991年，5岁的杨幂又在香港动作喜剧片《[武状元苏乞儿](/item/%E6%AD%A6%E7%8A%B6%E5%85%83%E8%8B%8F%E4%B9%9E%E5%84%BF/0?fromModule=lemma_inlink)》中露相，饰演男主角苏灿女儿，从此，开启了其演艺之路 [466] [499]。

[![](https://bkimg.cdn.bcebos.com/pic/a75fb6d3efd9cd6b960a1602?x-bce-process=image/format,f_auto/resize,m_lfit,limit_1,h_496)](/pic/%E6%9D%A8%E5%B9%82/149851/0/a75fb6d3efd9cd6b960a1602?fr=lemma&fromModule=lemma_content-image "杨幂童年与父亲合影")杨幂童年与父亲合影 [600]

1992年，杨幂与[六小龄童](/item/%E5%85%AD%E5%B0%8F%E9%BE%84%E7%AB%A5/0?fromModule=lemma_inlink)合作主演了戏曲题材儿童剧《[猴娃](/item/%E7%8C%B4%E5%A8%83/78485?fromModule=lemma_inlink)》，此剧在播出后则获得了第十四届“[飞天奖](/item/%E9%A3%9E%E5%A4%A9%E5%A5%96/0?fromModule=lemma_inlink)”少儿电视连续剧二等奖，而只有6岁的她也给该剧的制片人[李小婉](/item/%E6%9D%8E%E5%B0%8F%E5%A9%89/0?fromModule=lemma_inlink)留下了深刻的印象 [7] [499]。

1993年，杨幂在[李丹阳](/item/%E6%9D%8E%E4%B8%B9%E9%98%B3/19461?fromModule=lemma_inlink)的《[穿军装的川妹子](/item/%E7%A9%BF%E5%86%9B%E8%A3%85%E7%9A%84%E5%B7%9D%E5%A6%B9%E5%AD%90/0?fromModule=lemma_inlink)》MV中饰演小李丹阳， [12]而该作品则荣获了首届[中国音乐电视大赛](/item/%E4%B8%AD%E5%9B%BD%E9%9F%B3%E4%B9%90%E7%94%B5%E8%A7%86%E5%A4%A7%E8%B5%9B/0?fromModule=lemma_inlink)金奖 [500]。1996年，她还在[何晴](/item/%E4%BD%95%E6%99%B4/975354?fromModule=lemma_inlink)、[李亚鹏](/item/%E6%9D%8E%E4%BA%9A%E9%B9%8F/335118?fromModule=lemma_inlink)出演的青春电影《[歌手](/item/%E6%AD%8C%E6%89%8B/100559?fromModule=lemma_inlink)》中饰演了小夏表妹的角色。

2001年，15岁的杨幂在[北京市第十四中学](/item/%E5%8C%97%E4%BA%AC%E5%B8%82%E7%AC%AC%E5%8D%81%E5%9B%9B%E4%B8%AD%E5%AD%A6/5485924?fromModule=lemma_inlink)读初二，她在同学的建议下把自己的照片寄给了《瑞丽》时尚杂志社，在被编辑选中后开始做起了平面模特的工作 [497]。2002年，她签约了[李小婉](/item/%E6%9D%8E%E5%B0%8F%E5%A9%89/9279042?fromModule=lemma_inlink)、[李少红](/item/%E6%9D%8E%E5%B0%91%E7%BA%A2/4555992?fromModule=lemma_inlink)共同创办的[北京荣信达影视艺术有限公司](/item/%E5%8C%97%E4%BA%AC%E8%8D%A3%E4%BF%A1%E8%BE%BE%E5%BD%B1%E8%A7%86%E8%89%BA%E6%9C%AF%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/0?fromModule=lemma_inlink)。 [14]

2003年9月，杨幂拿到了她人生中的第一个剧本《[红粉世家](/item/%E7%BA%A2%E7%B2%89%E4%B8%96%E5%AE%B6/14253?fromModule=lemma_inlink)》，在剧中饰演女三号 [13] [15]；2004年6月，还在读高二的杨幂与[黄晓明](/item/%E9%BB%84%E6%99%93%E6%98%8E/6597?fromModule=lemma_inlink)、[刘亦菲](/item/%E5%88%98%E4%BA%A6%E8%8F%B2/136156?fromModule=lemma_inlink)等人共同出演了[金庸](/item/%E9%87%91%E5%BA%B8/128951?fromModule=lemma_inlink)武侠爱情剧《[神雕侠侣](/item/%E7%A5%9E%E9%9B%95%E4%BE%A0%E4%BE%A3/8065048?fromModule=lemma_inlink)》，并在剧中饰演了乖巧精灵的郭襄一角 [17]，而杨幂饰演的郭襄更是深得香港观众喜爱，被普遍认为是有史以来最清纯的郭襄 [471]。该剧也成立杨幂的成名作，使其在娱乐圈崭露头角，并获得了更多的发展机会 [19] [503]。

2005年，杨幂以专业课第一的成绩考入[北京电影学院](/item/%E5%8C%97%E4%BA%AC%E7%94%B5%E5%BD%B1%E5%AD%A6%E9%99%A2/0?fromModule=lemma_inlink)表演学院表演系，一边读书一边工作 [469] [501]；10月，她出演了电视电影《[北京童话](/item/%E5%8C%97%E4%BA%AC%E7%AB%A5%E8%AF%9D/0?fromModule=lemma_inlink)》，并饰演了白血病女孩朱珠 [16]；11月，她在古装人物传奇剧《[王昭君](/item/%E7%8E%8B%E6%98%AD%E5%90%9B/4424411?fromModule=lemma_inlink)》的女主角选拔中胜出，顺利在剧中饰演了中国古代四大美人之一的王昭君，并凭借该剧获得了第24届中国电视金鹰奖观众喜爱的电视剧女演员奖提名 [18] [502]；12月，杨幂与[胡歌](/item/%E8%83%A1%E6%AD%8C/312718?fromModule=lemma_inlink)搭档主演了古装奇幻剧《[聊斋志异之小倩](/item/%E8%81%8A%E6%96%8B%E5%BF%97%E5%BC%82%E4%B9%8B%E5%B0%8F%E5%80%A9/0?fromModule=lemma_inlink)》，并在剧中饰演了清丽脱俗的女主角[聂小倩](/item/%E8%81%82%E5%B0%8F%E5%80%A9/19135445?fromModule=lemma_inlink) [502]。2006年，杨幂一边读书，一边兼顾拍戏，并在《[相逢何必曾相识](/item/%E7%9B%B8%E9%80%A2%E4%BD%95%E5%BF%85%E6%9B%BE%E7%9B%B8%E8%AF%86/18043?fromModule=lemma_inlink)》《[门](/item/%E9%97%A8/3975713?fromModule=lemma_inlink)》等影视剧中出演角色 [504]。

2007年，杨幂先是在表演课年度考试作品《北京人》中饰演愫方 [20]；6月，她又在[北京电影学院](/item/%E5%8C%97%E4%BA%AC%E7%94%B5%E5%BD%B1%E5%AD%A6%E9%99%A2/0?fromModule=lemma_inlink)表演系05级学生表演专业课汇报演出中领衔主演了独幕剧《[青春禁忌游戏](/item/%E9%9D%92%E6%98%A5%E7%A6%81%E5%BF%8C%E6%B8%B8%E6%88%8F/23229911?fromModule=lemma_inlink)》，并在剧中饰演了拜金女高中生“拉拉” [21-22]；此外，12月，杨幂还在[北京电影学院](/item/%E5%8C%97%E4%BA%AC%E7%94%B5%E5%BD%B1%E5%AD%A6%E9%99%A2/224276?fromModule=lemma_inlink)表演系的年终舞台剧《楼梯的故事》中反串饰演了一个小男孩 [23]。

2003-2007年杨幂部分影视作品角色照

2008年7月7日，杨幂开始与众多艺人共同出演[李少红](/item/%E6%9D%8E%E5%B0%91%E7%BA%A2/4555992?fromModule=lemma_inlink)版《[红楼梦](/item/%E7%BA%A2%E6%A5%BC%E6%A2%A6/10578594?fromModule=lemma_inlink)》，并在剧中饰演了风流灵巧且口齿伶俐的俏丫鬟晴雯 [24]，虽然在剧中的戏份不多，但她却在拍摄中经历了“红色指甲不能摘”“连哭三天泪不断”“暑天卧床风沙袭脸”的三大考验，该剧播出之后，杨幂也凭借该角色获得观众好评 [25-27]；8月中旬，杨幂接到了《[仙剑奇侠传三](/item/%E4%BB%99%E5%89%91%E5%A5%87%E4%BE%A0%E4%BC%A0%E4%B8%89/5128963?fromModule=lemma_inlink)》剧组的邀请；之后，在经过与《[红楼梦](/item/%E7%BA%A2%E6%A5%BC%E6%A2%A6/10578594?fromModule=lemma_inlink)》剧组的再三商议后，《仙三》剧组最终成功“借”到了杨幂 [28-29]，而她在剧中则一人分饰了性格和气质截然不同的夕瑶和雪见，该剧在播出后取得了不俗的收视成绩，其个人也因此获得了更多关注 [30]；与此同时，杨幂还凭借《王昭君》入围第24届中国电视金鹰奖“最佳女主角”提名初选名单 [505]，此外，杨幂还在这一年出演了爱情剧《[暗香](/item/%E6%9A%97%E9%A6%99/15093?fromModule=lemma_inlink)》 [29]。

2009年4月，杨幂在由百万民众参与，近百名娱乐记者联合票选的“80后新生代娱乐大明星”评选中与[黄圣依](/item/%E9%BB%84%E5%9C%A3%E4%BE%9D/0?fromModule=lemma_inlink)、[王珞丹](/item/%E7%8E%8B%E7%8F%9E%E4%B8%B9/0?fromModule=lemma_inlink)、[刘亦菲](/item/%E5%88%98%E4%BA%A6%E8%8F%B2/136156?fromModule=lemma_inlink)共同获得了内地新“[四小花旦](/item/%E5%9B%9B%E5%B0%8F%E8%8A%B1%E6%97%A6/0?fromModule=lemma_inlink)”的称号 [1]；此外，她还与林心如、 王丽坤、陈键锋等人联袂出演了古装传奇宫斗剧《[美人心计](/item/%E7%BE%8E%E4%BA%BA%E5%BF%83%E8%AE%A1/24855?fromModule=lemma_inlink)》，并在剧中饰演了冷艳高傲且武功高强的绝色美人[莫雪鸢](/item/%E8%8E%AB%E9%9B%AA%E9%B8%A2/3455697?fromModule=lemma_inlink) [31]。

2008-2009年杨幂部分影视作品角色照

2010年，杨幂与荣信达公司的合约到期后，签约了香港美亚娱乐 [14] [32]；随后杨幂的事业呈多栖化发展，不仅所主演的电视剧《[神探狄仁杰前传](/item/%E7%A5%9E%E6%8E%A2%E7%8B%84%E4%BB%81%E6%9D%B0%E5%89%8D%E4%BC%A0/5404256?fromModule=lemma_inlink)》和《美人心计》均创下收视新高，还推出了自己进军歌坛的第一支歌曲《琉璃月》；在拍电视剧唱歌之余，她更马不停蹄狂见香港多位著名导演和制片人 [506]；同年，杨幂还主演了现代都市言情剧《[北京爱情故事](/item/%E5%8C%97%E4%BA%AC%E7%88%B1%E6%83%85%E6%95%85%E4%BA%8B/28263?fromModule=lemma_inlink)》 [148]，并凭借该剧获得了[第26届中国电视金鹰奖](/item/%E7%AC%AC26%E5%B1%8A%E4%B8%AD%E5%9B%BD%E7%94%B5%E8%A7%86%E9%87%91%E9%B9%B0%E5%A5%96/0?fromModule=lemma_inlink)“观众最喜爱的电视剧女演员”奖提名 [507-508]；此外，她还出演了好莱坞魔幻片《[人鱼帝国](/item/%E4%BA%BA%E9%B1%BC%E5%B8%9D%E5%9B%BD/7975474?fromModule=lemma_inlink)》 [509]。

《北京爱情故事》中饰演杨紫曦

2011年，杨幂主演的宫斗穿越剧《[宫锁心玉](/item/%E5%AE%AB%E9%94%81%E5%BF%83%E7%8E%89/1224780?fromModule=lemma_inlink)》开播，她在剧中饰演了意外回到康熙晚期的二十一世纪美少女洛晴川，该剧在播出期间一直位居全国同时段收视率第一的位置，同时也获得了上亿次的网络播放量。杨幂个人则凭借该剧首次登上了福布斯中国名人榜，并获得第17届上海电视节“白玉兰”奖“最具人气女演员”奖，提名该届“白玉兰奖”最佳女演员奖；奠定了她古装剧女神的地位 [510]。而由她演唱的《[宫](/item/%E5%AE%AB/5952473?fromModule=lemma_inlink)》剧主题曲《[爱的供养](/item/%E7%88%B1%E7%9A%84%E4%BE%9B%E5%85%BB/5715264?fromModule=lemma_inlink)》则登上了中国内地多个试听网站的冠军位置 [33]；7月8日，杨幂主演的悬疑惊悚片《[孤岛惊魂](/item/%E5%AD%A4%E5%B2%9B%E6%83%8A%E9%AD%82/8060879?fromModule=lemma_inlink)》在全国公映 [34-35]，在荧幕上一贯以清纯、甜美形象示人的杨幂，在该片中出演热爱探险、性格独立的靓丽美女沈伊琳。为演好这一角色，杨幂在片中会突破以往尺度，以性感比基尼扮相出场，因而备受关注 [511]。该片则最终凭借粉丝力量，创下了9000万的国产恐怖片票房纪录 [512]；9月12日，杨幂签约[少城时代](/item/%E5%B0%91%E5%9F%8E%E6%97%B6%E4%BB%A3/0?fromModule=lemma_inlink)，并加盟环球音乐，正式进军歌坛 [36]；而在谷歌公布的年度全球最热门搜索关键词排行榜中国地区人物搜索榜单中，她也最终排名榜首 [513]。

2012年，[杨幂工作室](/item/%E6%9D%A8%E5%B9%82%E5%B7%A5%E4%BD%9C%E5%AE%A4/0?fromModule=lemma_inlink)成立。1月4日，她的首张个人音乐专辑《[亲幂关系Close to Me](/item/%E4%BA%B2%E5%B9%82%E5%85%B3%E7%B3%BBClose%20to%20Me/0?fromModule=lemma_inlink)》正式发行 [37] [474]；3月6日，其担任制作人的青春偶像剧《[中国女孩](/item/%E4%B8%AD%E5%9B%BD%E5%A5%B3%E5%AD%A9/4329829?fromModule=lemma_inlink)》启动，而这也是她首次担任影视制作人 [514]；随后，杨幂在福布斯中国名人榜中从前一年的第92名升至第13位 [515]，并在福布斯中国微博名人榜中位列第2 [516]；而在“华鼎亚洲演艺名人满意度调查”国内新锐百强榜的调查过程中，她则以876.68分排名榜首 [38]；7月，其领衔主演的夺宝动作片《[大武当之天地密码](/item/%E5%A4%A7%E6%AD%A6%E5%BD%93%E4%B9%8B%E5%A4%A9%E5%9C%B0%E5%AF%86%E7%A0%81/6675651?fromModule=lemma_inlink)》在全国公映，她在片中饰演天心，而该片也是杨幂的动作片首秀 [39] [130] [517]；8月，由其自导自演的首部微电影作品《[交换旅行](/item/%E4%BA%A4%E6%8D%A2%E6%97%85%E8%A1%8C/10103257?fromModule=lemma_inlink)》也在优酷网同期首发播映 [40]；9月9日，杨幂在[第26届中国电视金鹰奖](/item/%E7%AC%AC26%E5%B1%8A%E4%B8%AD%E5%9B%BD%E7%94%B5%E8%A7%86%E9%87%91%E9%B9%B0%E5%A5%96/0?fromModule=lemma_inlink)颁奖典礼上获得了最具人气女演员奖 [41]。

2008-2009年杨幂部分影视作品角色照

2013年6月27日，其领衔主演的根据[郭敬明](/item/%E9%83%AD%E6%95%AC%E6%98%8E/158248?fromModule=lemma_inlink)同名小说改编并由他自编自导的都市青春片《[小时代](/item/%E5%B0%8F%E6%97%B6%E4%BB%A3/6737508?fromModule=lemma_inlink)》首映，她在片中则饰演了温和善良、胆小怕事，却又从不气馁的第一女主角林萧 [120] [518]，该片也以排片45.01%，全国放映约3.5万场，创造了华语电影首日排片纪录，而超过210万的观影人次、约7300万元人民币的票房，也创造了中国2D电影的首日票房纪录 [43-44] [120-121]；8月，杨幂还获得了亚洲偶像盛典年度最具实力制作人 [45]；9月，杨幂还在当年的福布斯中国名人榜中排名第七 [521]。

2014年6月27日，她主演的由邓超自导自演的现代剧情片《[分手大师](/item/%E5%88%86%E6%89%8B%E5%A4%A7%E5%B8%88/10266867?fromModule=lemma_inlink)》上映，并担任了该片的女主角，北漂女叶小春 [46-47] [115]；7月17日，杨幂主演的《[小时代3：刺金时代](/item/%E5%B0%8F%E6%97%B6%E4%BB%A33%EF%BC%9A%E5%88%BA%E9%87%91%E6%97%B6%E4%BB%A3/12702233?fromModule=lemma_inlink)》首映，并在首日取得了1.1亿元人民币（含点映场及零点首映），排片占比44%的票房成绩；而其首映成绩便收获了750万元人民币，零点场排片1500多场，与《小时代1》的800场先后创下了零点场纪录 [48] [113-114]；7月21日，杨幂首次担任了电视剧制片人，她与欢瑞世纪共同制作了都市爱情剧《[微时代](/item/%E5%BE%AE%E6%97%B6%E4%BB%A3/7626967?fromModule=lemma_inlink)》播出，并在剧中本色饰演了影视明星洛依 [42] [519] [617]；随后，她主演的《分手大师》《小时代3》近12亿的票房让她成为2014年首位进入“10亿票房女主俱乐部”的艺人 [49]；在电视和网络方面，其主演的古装仙侠偶像剧《[古剑奇谭](/item/%E5%8F%A4%E5%89%91%E5%A5%87%E8%B0%AD/5016869?fromModule=lemma_inlink)》在播放期间获得了全国同时段电视剧收视率第一，网络播放量突破50亿，单集平均点击量则突破1.5亿，单日播放量9447万的成绩 [50]。

2013-2014年杨幂部分影视作品角色照

2015年，杨幂与两位经纪人[赵若尧](/item/%E8%B5%B5%E8%8B%A5%E5%B0%A7/0?fromModule=lemma_inlink)、[曾嘉](/item/%E6%9B%BE%E5%98%89/4912159?fromModule=lemma_inlink)共同出资300万人民币成立了海宁嘉行天下影视文化有限公司 [487]，并于随后签下了自立门户后的第一批艺人 [51-52]；4月30日，她与[黄晓明](/item/%E9%BB%84%E6%99%93%E6%98%8E/6597?fromModule=lemma_inlink)搭档主演的都市爱情片《[何以笙箫默](/item/%E4%BD%95%E4%BB%A5%E7%AC%99%E7%AE%AB%E9%BB%98/15839668?fromModule=lemma_inlink)》上映，该片首周票房便突破2.2亿人民币，总票房则达到了3.5亿人民币 [55-56] [112] [433]；7月，其主演的《[小时代4：灵魂尽头](/item/%E5%B0%8F%E6%97%B6%E4%BB%A34%EF%BC%9A%E7%81%B5%E9%AD%82%E5%B0%BD%E5%A4%B4/14917071?fromModule=lemma_inlink)》上映，累计票房达到4.82亿元，随着《小时代》系列的完结，该片最终票房成绩超过了18亿人民币，并创造了国产系列电影的票房纪录 [48] [520]；10月，欢瑞杨幂工作室更名为嘉行杨幂工作室 [487]；10月30日，杨幂与[鹿晗](/item/%E9%B9%BF%E6%99%97/0?fromModule=lemma_inlink)搭档主演了现代悬疑剧情片《[我是证人](/item/%E6%88%91%E6%98%AF%E8%AF%81%E4%BA%BA/16785929?fromModule=lemma_inlink)》上映，并在片中饰演了虽然双目失明却正义凛然的命案目击者路小星 [57] [522] [616]；11月，杨幂产后复工，并出演了现代言情片《[恋爱中的城市](/item/%E6%81%8B%E7%88%B1%E4%B8%AD%E7%9A%84%E5%9F%8E%E5%B8%82/15852854?fromModule=lemma_inlink)》 [53-54]；12月3日，杨幂主演了浪漫爱情喜剧片《[怦然星动](/item/%E6%80%A6%E7%84%B6%E6%98%9F%E5%8A%A8/17604559?fromModule=lemma_inlink)》上映，她片中饰演金牌经纪人田心 [58] [110-111] [615]。

2016年6月，其主演的职场爱情剧《[亲爱的翻译官](/item/%E4%BA%B2%E7%88%B1%E7%9A%84%E7%BF%BB%E8%AF%91%E5%AE%98/16910157?fromModule=lemma_inlink)》播出，她在剧中饰演美丽知性且倔强独立的女主角乔菲 [141-142] [524]，而该剧自开播以来就保持较高热度，曾创造全国网单集破4的记录，更凭借双网破2的收视率取得了全国年度电视剧收视冠军 [525-526]；9月30日，杨幂作为特别嘉宾出演电影《[爵迹](/item/%E7%88%B5%E8%BF%B9/16997856?fromModule=lemma_inlink)》在全国公映，她在片中饰演性格开朗并拥有痊愈天赋的神族少女神音 [612-613]，该片上映4天取得近2.5亿的票房 [527-528]；10月21日，其参加的国防教育真人秀《[真正男子汉第二季](/item/%E7%9C%9F%E6%AD%A3%E7%94%B7%E5%AD%90%E6%B1%89%E7%AC%AC%E4%BA%8C%E5%AD%A3/0?fromModule=lemma_inlink)》开始在湖南卫视播出，而杨幂则与其他几位嘉宾共同深入一线部队，在空军的各个兵种内经历了五次三天两晚的真实军营体验 [60] [614]，在电视剧领域屡创新高的杨幂，却在荧幕之旅不太顺遂。同年，她凭借《小时代4：灵魂尽头》《何以笙箫默》两部电影获得第七届中国电影金扫帚奖获最令人失望女演员奖，这是她第三次获得该奖项 [529]。

2015-2016年杨幂部分影视作品角色照

2017年1月，杨幂主演的古装神话爱情剧《[三生三世十里桃花](/item/%E4%B8%89%E7%94%9F%E4%B8%89%E4%B8%96%E5%8D%81%E9%87%8C%E6%A1%83%E8%8A%B1/16246274?fromModule=lemma_inlink)》在东方卫视、浙江卫视以及众网络平台开播，她在剧中饰演了敢爱敢恨的九尾白狐族上神、青丘帝姬白浅 [61-62]，该剧在收官时收获双台连续破1的收视成绩、一路高歌逼近300亿网播数据 [63]，而杨幂也因此得到了更多观众的认可 [64]，并连续成为了各热搜指数的话题人物 [65]；2月28日，杨幂被聘任为了中国电视艺术家协会演员工作委员会理事 [66]；6月29日，她还领衔主演了中韩合拍的科幻动作片《[逆时营救](/item/%E9%80%86%E6%97%B6%E8%90%A5%E6%95%91/20601217?fromModule=lemma_inlink)》上映，其在片中饰演了身为物理研究员的单亲妈妈夏天 [109] [611]，凭借此片获得第50届休斯敦国际电影节最佳女主角奖，而这也是她拿下的首个国际电影节最佳女主角奖项 [2]；在这一年，杨幂在福布斯中国名人榜中的排名跃居第3位 [530]；7月19日，杨幂主演古装动作电影《[绣春刀Ⅱ：修罗战场](/item/%E7%BB%A3%E6%98%A5%E5%88%80%E2%85%A1%EF%BC%9A%E4%BF%AE%E7%BD%97%E6%88%98%E5%9C%BA/20393681?fromModule=lemma_inlink)》上映，并在片中饰演神秘的画师[北斋](/item/%E5%8C%97%E6%96%8B/23287627?fromModule=lemma_inlink) [59] [107-108]，并凭借此片获得北京大学生电影节最受大学生欢迎女演员奖 [3] [523]；12月31日，她还参加了东方卫视跨年晚会，在晚会上杨幂除了与[张杰](/item/%E5%BC%A0%E6%9D%B0/256?fromModule=lemma_inlink)搭档表演了歌曲《[三生三世](/item/%E4%B8%89%E7%94%9F%E4%B8%89%E4%B8%96/20375578?fromModule=lemma_inlink)》之外，还展示了书法才艺 [67]。

2018年2月，杨幂主演的都市时尚剧《[谈判官](/item/%E8%B0%88%E5%88%A4%E5%AE%98/20139873?fromModule=lemma_inlink)》在[湖南卫视](/item/%E6%B9%96%E5%8D%97%E5%8D%AB%E8%A7%86/220836?fromModule=lemma_inlink)播出，她在剧中饰演的女主角[童薇](/item/%E7%AB%A5%E8%96%87/22356743?fromModule=lemma_inlink)是CAEA高级谈判专家，专业功底扎实、谈判风格胆大心细 [68] [140]，而该剧在首播就获得收视破1的好成绩，年轻人群份额破9%，在年轻观众群体中受关注度高 [69]；6月18日，杨幂领衔主演的古装剧《[扶摇](/item/%E6%89%B6%E6%91%87/20216615?fromModule=lemma_inlink)》在浙江卫视播出，其在剧中饰演的是平凡却努力蓄积力量成长的[扶摇](/item/%E6%89%B6%E6%91%87/20216615?fromModule=lemma_inlink) [70]；8月17日，杨幂主演的个人首部文艺片《[宝贝儿](/item/%E5%AE%9D%E8%B4%9D%E5%84%BF/22291142?fromModule=lemma_inlink)》入围第43届多伦多国际电影节“特别展映”单元、第66届圣塞巴斯蒂安国际电影节主竞赛单元 [71]；12月28日，杨幂获得了[第五届中国电视好演员奖](/item/%E7%AC%AC%E4%BA%94%E5%B1%8A%E4%B8%AD%E5%9B%BD%E7%94%B5%E8%A7%86%E5%A5%BD%E6%BC%94%E5%91%98%E5%A5%96/56467070?fromModule=lemma_inlink)绿宝石女演员奖 [4]；而其领衔主演的奇幻动作悬疑片《[刺杀小说家](/item/%E5%88%BA%E6%9D%80%E5%B0%8F%E8%AF%B4%E5%AE%B6/19776773?fromModule=lemma_inlink)》也于同年开拍 [72]。

2019年，身为北京人的杨幂担任了北京电视台春节联欢晚会的代言人 [73]，并在晚会与[蔡徐坤](/item/%E8%94%A1%E5%BE%90%E5%9D%A4/8511458?fromModule=lemma_inlink)合作表演了主题秀《[那年春天](/item/%E9%82%A3%E5%B9%B4%E6%98%A5%E5%A4%A9/24188670?fromModule=lemma_inlink)》 [74]，而晚会播出后则以破2的实时关注度和12.165%的市占率，成为该年卫视春晚冠军 [75]。随后，除了以固定嘉宾身份参加了芒果TV室内真人秀《[密室大逃脱](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1/23317967?fromModule=lemma_inlink)》 [76]，她还在CCTV-1黄金档播出的《我们都是追梦人—— “五月的鲜花”全国大中学生文艺会演》中与[魏大勋](/item/%E9%AD%8F%E5%A4%A7%E5%8B%8B/5264432?fromModule=lemma_inlink)合作演唱了歌曲《青春畅想》 [77]；5月6日，主演的年代励志剧《[筑梦情缘](/item/%E7%AD%91%E6%A2%A6%E6%83%85%E7%BC%98/23449117?fromModule=lemma_inlink)》在湖南卫视金播出，她在剧中饰演的是建筑设计师傅函君； [78] [531]7月，其作为梦想观察员参加的东方卫视选秀节目《[中国达人秀第六季](/item/%E4%B8%AD%E5%9B%BD%E8%BE%BE%E4%BA%BA%E7%A7%80%E7%AC%AC%E5%85%AD%E5%AD%A3/23628606?fromModule=lemma_inlink)》播出 [79]；12月27日，客串出演的国庆70周年献礼片《[解放·终局营救](/item/%E8%A7%A3%E6%94%BE%C2%B7%E7%BB%88%E5%B1%80%E8%90%A5%E6%95%91/23750072?fromModule=lemma_inlink)》上映，杨幂在片中饰演蔡兴福的妻子何秀萍，并在剧中首次挑战旗袍造型，并在当天“喜提热搜” [80-82]；而其在这一年的[福布斯中国名人榜](/item/%E7%A6%8F%E5%B8%83%E6%96%AF%E4%B8%AD%E5%9B%BD%E5%90%8D%E4%BA%BA%E6%A6%9C/2125?fromModule=lemma_inlink)上则位列第9 [83]。

2020年1月，杨幂友情出演的古装神话爱情剧《[三生三世枕上书](/item/%E4%B8%89%E7%94%9F%E4%B8%89%E4%B8%96%E6%9E%95%E4%B8%8A%E4%B9%A6/15821930?fromModule=lemma_inlink)》播出，她在剧中也再次饰演了白浅 [84]；6月30日，担任常驻嘉宾的实景解密体验秀《[密室大逃脱第二季](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1%E7%AC%AC%E4%BA%8C%E5%AD%A3/50034401?fromModule=lemma_inlink)》在芒果TV播出 [86]；随后，她入选福布斯中国名人榜，排名是第六位 [87]；9月，杨幂以42218的票数获得第30届中国电视金鹰奖观众喜爱的女演员奖提名 [88]；11月，参演的中国首部女性独白综艺单元剧《[听见她说](/item/%E5%90%AC%E8%A7%81%E5%A5%B9%E8%AF%B4/53096726?fromModule=lemma_inlink)》播出 [89]；同年，她还以导师身份参加了语言达人秀《[奇葩说第七季](/item/%E5%A5%87%E8%91%A9%E8%AF%B4%E7%AC%AC%E4%B8%83%E5%AD%A3/51145073?fromModule=lemma_inlink)》 [90]。

2015-2020年杨幂部分影视作品角色照

2021年1月，杨幂与其他五位艺人共同担任了中央广播电视总台春节特别节目《[中国声音中国年](/item/%E4%B8%AD%E5%9B%BD%E5%A3%B0%E9%9F%B3%E4%B8%AD%E5%9B%BD%E5%B9%B4/22389673?fromModule=lemma_inlink)》宣传推广大使 [91]；并在2月11日的中央广播电视总台春节联欢晚会上与[刘烨](/item/%E5%88%98%E7%83%A8/13286?fromModule=lemma_inlink)、[李沁](/item/%E6%9D%8E%E6%B2%81/7055?fromModule=lemma_inlink)等人共同演唱《[燃烧的雪花](/item/%E7%87%83%E7%83%A7%E7%9A%84%E9%9B%AA%E8%8A%B1/56080600?fromModule=lemma_inlink)》 [443] [532]；2月12日，主演的奇幻冒险片《[刺杀小说家](/item/%E5%88%BA%E6%9D%80%E5%B0%8F%E8%AF%B4%E5%AE%B6/19776773?fromModule=lemma_inlink)》上映；杨幂在其中饰演从小被遗弃、面对老板下达的指令绝对服从的打手屠灵 [106] [533]；2月23日，主演的现代都市反谍剧《[暴风眼](/item/%E6%9A%B4%E9%A3%8E%E7%9C%BC/23280738?fromModule=lemma_inlink)》播出，其在剧中饰演了国安局侦察科长安静 [92-93]；5月6日，作为固定嘉宾参加的真人秀《[密室大逃脱第三季](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1%E7%AC%AC%E4%B8%89%E5%AD%A3/56597815?fromModule=lemma_inlink)》开播 [361]；11月10日，其与[陈伟霆](/item/%E9%99%88%E4%BC%9F%E9%9C%86/3463936?fromModule=lemma_inlink)搭档主演的古装传奇剧《[斛珠夫人](/item/%E6%96%9B%E7%8F%A0%E5%A4%AB%E4%BA%BA/50009318?fromModule=lemma_inlink)》在腾讯视频播出，杨幂在剧中饰演的“斛珠夫人”海市，是位在纷繁复杂的权力斗争中，坚守和平与真爱的传奇女子，凭借原著小说的吸引力以及强大的主演阵容，该剧在开播前便稳居灯塔专业版网剧热度榜前十位，同时剧集预告片破亿，且微博话题“杨幂斛珠夫人”阅读量超达到29.4亿次 [85] [368-369] [534]；12月31日，她还参加了湖南卫视跨年晚会，并与[周笔畅](/item/%E5%91%A8%E7%AC%94%E7%95%85/129239?fromModule=lemma_inlink)合作演唱了歌曲《[小幸运](/item/%E5%B0%8F%E5%B9%B8%E8%BF%90/18028059?fromModule=lemma_inlink)》 [394]；而在这一年的福布斯中国名人榜上，杨幂则位列第四 [365]。

2022年2月，杨幂参加的《[中国梦·我的梦——中国网络视听年度盛典](/item/%E4%B8%AD%E5%9B%BD%E6%A2%A6%C2%B7%E6%88%91%E7%9A%84%E6%A2%A6%E2%80%94%E2%80%94%E4%B8%AD%E5%9B%BD%E7%BD%91%E7%BB%9C%E8%A7%86%E5%90%AC%E5%B9%B4%E5%BA%A6%E7%9B%9B%E5%85%B8/59942537?fromModule=lemma_inlink)》上线播出 [400]；随后，她还参加了《百花迎春——中国文学艺术界春节大联欢》，并在晚会上演唱了歌曲《岁月》 [397]；6月17日，作为固定嘉宾参加的湖南卫视自助旅行真人秀《[花儿与少年第四季](/item/%E8%8A%B1%E5%84%BF%E4%B8%8E%E5%B0%91%E5%B9%B4%E7%AC%AC%E5%9B%9B%E5%AD%A3/61270992?fromModule=lemma_inlink)》播出 [411]；7月14日，作为固定嘉宾参加的真人秀《[密室大逃脱第四季](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1%E7%AC%AC%E5%9B%9B%E5%AD%A3/60413188?fromModule=lemma_inlink)》开播 [414]；此外，她还以主要嘉宾的身份参加了电竞实训节目《[战至巅峰](/item/%E6%88%98%E8%87%B3%E5%B7%85%E5%B3%B0/61287755?fromModule=lemma_inlink)》 [417-418]；11月，杨幂主演的两部电视剧开播分别是都市医疗情感剧 《[谢谢你医生](/item/%E8%B0%A2%E8%B0%A2%E4%BD%A0%E5%8C%BB%E7%94%9F/24141892?fromModule=lemma_inlink)》和现代都市爱情剧《[爱的二八定律](/item/%E7%88%B1%E7%9A%84%E4%BA%8C%E5%85%AB%E5%AE%9A%E5%BE%8B/23664662?fromModule=lemma_inlink)》 [420-421] [423]；11月30日，参演的综艺节目《[红毯背后](/item/%E7%BA%A2%E6%AF%AF%E8%83%8C%E5%90%8E/62390527?fromModule=lemma_inlink)》播出，她在节目中则担任了“特邀导师” [428]；12月31日，连续第二年参加湖南卫视跨年晚会，并与[大张伟](/item/%E5%A4%A7%E5%BC%A0%E4%BC%9F/405253?fromModule=lemma_inlink)共同演唱歌曲《一个nice》《你怎么这么好看》《月亮代表我的心》 [429-430]。

2023年1月14日，杨幂参加了快手[老铁联欢晚会](/item/%E8%80%81%E9%93%81%E8%81%94%E6%AC%A2%E6%99%9A%E4%BC%9A/62534526?fromModule=lemma_inlink) [431]；随后出席百度沸点元宇宙之夜 [432]；1月22日，她又受邀参加“百花迎春”——中国文学艺术界春节大联欢 [434]；同年5月4日，参加的励志故事探寻节目《当燃青春》播出 [437]；此后，杨幂宣布与嘉行传媒解除合作关系 [438]；6月7日，作为固定嘉宾参加的真人秀《[密室大逃脱第五季](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1%E7%AC%AC%E4%BA%94%E5%AD%A3/62615867?fromModule=lemma_inlink)》开播 [440]；9月29日，参加的中央广播电视总台中秋晚会播出，其在晚会上则与[刘瑾睿](/item/%E5%88%98%E7%91%BE%E7%9D%BF/58400184?fromModule=lemma_inlink)共同演唱了歌曲《[若把你](/item/%E8%8B%A5%E6%8A%8A%E4%BD%A0/54732872?fromModule=lemma_inlink)》 [446]。此外，于12月，杨幂入选《智族GQ》2023年度艺人 [535]。

2024年2月7日，杨幂参加河南电视台春节晚会，并在晚会中演唱歌曲《入梦风华》 [454] [457]；两日后，她第二次参加中央广播电视总台春节联欢晚会，并参与表演了开场节目《[鼓舞龙腾](/item/%E9%BC%93%E8%88%9E%E9%BE%99%E8%85%BE/64050090?fromModule=lemma_inlink)》以及歌曲《[让幸福飞起来](/item/%E8%AE%A9%E5%B9%B8%E7%A6%8F%E9%A3%9E%E8%B5%B7%E6%9D%A5/64050021?fromModule=lemma_inlink)》 [460-461]；2月10日，其参演的百花迎春——中国文学艺术界春节大联欢播出，演唱歌曲《同路人》 [459]；3月22日，参与角色狐狸小真配音的动画电影《[功夫熊猫4](/item/%E5%8A%9F%E5%A4%AB%E7%86%8A%E7%8C%AB4/6003348?fromModule=lemma_inlink)》上映 [462]；3月，其出演的剧情片《[酱园弄](/item/%E9%85%B1%E5%9B%AD%E5%BC%84/63587172?fromModule=lemma_inlink)》杀青 [465]；4月21日，主演的原创年代谍战悬疑剧《[哈尔滨一九四四](/item/%E5%93%88%E5%B0%94%E6%BB%A8%E4%B8%80%E4%B9%9D%E5%9B%9B%E5%9B%9B/62881700?fromModule=lemma_inlink)》播出，在剧中，她首次饰演反派角色特务科长关雪 [439] [468] [536]；5月1日，主演的悬疑喜剧片《[没有一顿火锅解决不了的事](/item/%E6%B2%A1%E6%9C%89%E4%B8%80%E9%A1%BF%E7%81%AB%E9%94%85%E8%A7%A3%E5%86%B3%E4%B8%8D%E4%BA%86%E7%9A%84%E4%BA%8B/62527597?fromModule=lemma_inlink)》上映，片中杨幂饰演一位性格泼辣的化妆品美女电商，名叫幺鸡 [449] [452] [463] [609-610]；5月8日，其登上《ELLE》6月刊封面，此次封面是以三封面开场 [601]；5月23日，领衔主演古装玄幻剧《[狐妖小红娘·月红篇](/item/%E7%8B%90%E5%A6%96%E5%B0%8F%E7%BA%A2%E5%A8%98%C2%B7%E6%9C%88%E7%BA%A2%E7%AF%87/61575204?fromModule=lemma_inlink)》播出，并在剧中饰演涂山狐族心怀大义的大当家涂山红红 [415] [419] [608]；8月5日，主演的年代剧《[生万物](/item/%E7%94%9F%E4%B8%87%E7%89%A9/64045372?fromModule=lemma_inlink)》杀青，在剧中饰演鲁南村妇宁绣绣 [634]；10月19日，参加VOGUE时尚之力盛会 [631]，并获得Force of Fashion Award时尚之力大奖“年度潮流引领者奖” [635]；10月26日，参加《战至巅峰第三季》总决赛 [632]；10月27日，杨幂作为荣耀王者代言人和惊喜嘉宾参加了王者荣耀共创之夜 [620] [633]。12月31日，参加《[2024-2025湖南卫视芒果TV跨年晚会](/item/2024-2025%E6%B9%96%E5%8D%97%E5%8D%AB%E8%A7%86%E8%8A%92%E6%9E%9CTV%E8%B7%A8%E5%B9%B4%E6%99%9A%E4%BC%9A/65181640?fromModule=lemma_inlink)》表演节目《异想记》 [636-637]。

2025年1月24日，参加的综艺《下班啦2024》播出。 [640]7月25日，参演的电影《长安的荔枝》上映。 [643-644]

2021-2025年杨幂部分影视作品角色照

2011年10月，杨幂出资30万元参股欢瑞世纪，并于2014年6月出资507万元又受让了20万股股份，共持股50万股，持股比例0.46% [95-96]。2015年7月，欢瑞世纪借壳泰亚股份前夕，杨幂将手中所持的50万股全部清空，转让给了浙江欢瑞 [97]。

2015年10月，杨幂与经纪人所创办的公司西藏嘉行以85万元收购了岳峰持有的西安同大50万股股份，加上此前西安同大向西藏嘉行增发的550万股，西藏嘉行持有西安同大股份的比例达到37%，上位西安同大第一大股东。 [98]

2021年6月，杨幂与父亲[杨晓林](/item/%E6%9D%A8%E6%99%93%E6%9E%97/20867510?fromModule=lemma_inlink)共同持股的海南慈爵文化传播合伙企业（有限合伙）成立 [363]。

2023年8月，杨幂宣布退出了北京世嘉华林文化传播有限责任公司，并卸任监事。该合作可追溯至2007年，她与曾嘉及其他合伙人共同创立嘉行传媒并签约多位艺人，嘉行传媒也因多部热门剧集在影视界崭露头角。此后，双方关系出现裂痕。2018年杨幂退出与曾嘉合作的企业，2020年开始使用上海杨幂影视文化工作室的名义落款， [537]2023年5月8日，杨幂正式宣布与嘉行传媒结束合作 [438]。

杨幂写真

个人生活
----

播报

编辑

2009年10月，杨幂在拍片现场收养了一只被遗弃的小猫，并给它取名为喜宝，因此收到了善待动物组织亚洲分部授予的“影响力”奖 [94]。

杨幂生活照

2011年，杨幂与[刘恺威](/item/%E5%88%98%E6%81%BA%E5%A8%81/3113102?fromModule=lemma_inlink)在拍摄电视剧《[如意](/item/%E5%A6%82%E6%84%8F/254841?fromModule=lemma_inlink)》时因戏生情。 [99-100]2012年，两人双双在个人微博承认已开始恋爱 [101]。

2014年1月8日，杨幂与刘恺威在巴厘岛举办了结婚典礼，而此前两人已领取了结婚证书； [102] [538]1月19日，刘恺威证实杨幂已怀孕3个多月 [103]；6月1日，杨幂在香港产下了女儿[小糯米](/item/%E5%B0%8F%E7%B3%AF%E7%B1%B3/1586135?fromModule=lemma_inlink) [104]。

2018年12月22日，杨幂和刘恺威发表声明，宣布已于年内离婚，之后两人会以亲人的身份共同抚养女儿 [105]。

2025年2月，杨幂在最新采访透露，滑雪时发现右胳膊难抬起来，去检查发现有些地方已经钙化。杨幂谈对这件事的看法：“会找到一个快乐点，比如我会说‘我变身了！’比起钙化这件事，找到快乐的角度很重要。” [642]

主要作品
----

播报

编辑

**[刁蛮新娘](/item/%E5%88%81%E8%9B%AE%E6%96%B0%E5%A8%98/9953043?fromModule=lemma_inlink) [162]****2010-10-23 [163]**

饰演
:   颜小蛮/戴小蛮

导演
:   [陈启峻](/item/%E9%99%88%E5%90%AF%E5%B3%BB/1474894?fromModule=lemma_inlink)

主演
:   [李东学](/item/%E6%9D%8E%E4%B8%9C%E5%AD%A6/8652380?fromModule=lemma_inlink)、孙坚、王琳

**[上书房](/item/%E4%B8%8A%E4%B9%A6%E6%88%BF/1581358?fromModule=lemma_inlink) [173]****2008-01-06 [174]**

饰演
:   富察敦儿

导演
:   [曾丽珍](/item/%E6%9B%BE%E4%B8%BD%E7%8F%8D/4121154?fromModule=lemma_inlink)

主演
:   袁弘、何苗、刘斌

发行时间2012-01-04

发行时间2012-01-04

专辑语言普通话

唱片公司少城时代

专辑类型录音室专辑

专辑简介

《[亲幂关系Close to Me](/item/%E4%BA%B2%E5%B9%82%E5%85%B3%E7%B3%BBClose%20to%20Me/0?fromModule=lemma_inlink)》录音制作地点横跨北京、香港、台湾两岸三地,在香港做造型,在台湾进行封面、内页和MV的拍摄,邀请到著名音乐人王治平、Dave Chan、吕绍淳、王菲的御用作曲C.Y. Kong、张惠妹的声乐老师陈秀珠以及林夕、陈奕迅、张靓颖等倾情加盟,精工细制打磨近半年时间。

专辑曲目不是秘密的秘密、爱快来、刺猬的拥抱、爱的讯号、叮咚、异想记、滴答、还过得去、需要恋爱的夏天、LALALA、爱的供养(新版)

| 歌曲名称 | 发行时间 | 歌曲简介 |
| --- | --- | --- |
| [入梦风华](/item/%E5%85%A5%E6%A2%A6%E9%A3%8E%E5%8D%8E/64046282?fromModule=lemma_inlink) | 2024-2-8 | 个人单曲 [458] |
| [心手相握](/item/%E5%BF%83%E6%89%8B%E7%9B%B8%E6%8F%A1/55593297?fromModule=lemma_inlink) | 2021-1-2 | 《浙江卫视2021跨年晚会》主题曲 [198-199] |
| [密室大逃脱](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1/53034966?fromModule=lemma_inlink) | 2020-6-30 | 综艺节目《密室大逃脱》主题曲 [541] |
| 她他 | 2014-07-28 | 网络剧《微时代》插曲 [542] |
| [一定要幸福](/item/%E4%B8%80%E5%AE%9A%E8%A6%81%E5%B9%B8%E7%A6%8F/972450?fromModule=lemma_inlink) | 2013-05-02 | 电视剧《盛夏晚晴天》插曲 [543] |
| [如果爱老了](/item/%E5%A6%82%E6%9E%9C%E7%88%B1%E8%80%81%E4%BA%86/6213893?fromModule=lemma_inlink) | 2013-02-22 | 电视剧《盛夏晚晴天》主题曲 [544] |
| [爱情地图](/item/%E7%88%B1%E6%83%85%E5%9C%B0%E5%9B%BE/48833?fromModule=lemma_inlink) | 2012-06-24 | 电影《大武当之天地密码》主题曲 [545] |
| [跑出一片天](/item/%E8%B7%91%E5%87%BA%E4%B8%80%E7%89%87%E5%A4%A9/18705584?fromModule=lemma_inlink) | 2012-05-08 | 电影《跑出一片天》主题曲 [546] |
| [有点舍不得](/item/%E6%9C%89%E7%82%B9%E8%88%8D%E4%B8%8D%E5%BE%97/9034444?fromModule=lemma_inlink) | 2012-01-29 | 电视剧《如意》片头曲 [547] |
| [错怪](/item/%E9%94%99%E6%80%AA/8510058?fromModule=lemma_inlink) | 2012-01-29 | 电视剧《如意》片尾曲 [547] |

| 播出时间 | 节目名称 | 备注信息 |
| --- | --- | --- |
| 2023年 | 《[密室大逃脱第五季](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1%E7%AC%AC%E4%BA%94%E5%AD%A3/62615867?fromModule=lemma_inlink)》 | [440] |
| 2022年 | 《[红毯背后](/item/%E7%BA%A2%E6%AF%AF%E8%83%8C%E5%90%8E/62390527?fromModule=lemma_inlink)》 | 担任特邀导师 [428] |
| 《[战至巅峰](/item/%E6%88%98%E8%87%B3%E5%B7%85%E5%B3%B0/61287755?fromModule=lemma_inlink)》 | 担任主要嘉宾 [412] |
| 《[密室大逃脱第四季](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1%E7%AC%AC%E5%9B%9B%E5%AD%A3/60413188?fromModule=lemma_inlink)》 | 担任固定嘉宾 [414] |
| 《[花儿与少年第四季](/item/%E8%8A%B1%E5%84%BF%E4%B8%8E%E5%B0%91%E5%B9%B4%E7%AC%AC%E5%9B%9B%E5%AD%A3/61270992?fromModule=lemma_inlink)》 | 担任节目固定嘉宾 [411] |
| 2021年 | 《[密室大逃脱第三季](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1%E7%AC%AC%E4%B8%89%E5%AD%A3/56597815?fromModule=lemma_inlink)》 | 担任固定嘉宾 [361] |
| 2020年 | 《[奇葩说第七季](/item/%E5%A5%87%E8%91%A9%E8%AF%B4%E7%AC%AC%E4%B8%83%E5%AD%A3/51145073?fromModule=lemma_inlink)》 | 担任节目导师 [90] |
| 《[听见她说](/item/%E5%90%AC%E8%A7%81%E5%A5%B9%E8%AF%B4/53096726?fromModule=lemma_inlink)》 | 出演的中国首部女性独白综艺剧 [200] |
| 《[上线吧！华彩少年](/item/%E4%B8%8A%E7%BA%BF%E5%90%A7%EF%BC%81%E5%8D%8E%E5%BD%A9%E5%B0%91%E5%B9%B4/53552400?fromModule=lemma_inlink)》 | 担任上线官、国风少年计划见证人 [201] |
| 《[密室大逃脱第二季](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1%E7%AC%AC%E4%BA%8C%E5%AD%A3/50034401?fromModule=lemma_inlink)》 | 担任固定嘉宾 [86] |
| 2019年 | 《[中国达人秀第六季](/item/%E4%B8%AD%E5%9B%BD%E8%BE%BE%E4%BA%BA%E7%A7%80%E7%AC%AC%E5%85%AD%E5%AD%A3/23628606?fromModule=lemma_inlink)》 | 担任节目梦想观察员 [79] |
| 《[密室大逃脱](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1/23317967?fromModule=lemma_inlink)》 | 芒果TV室内真人秀 [76] |
| 2018年 | 《[明日之子第二季](/item/%E6%98%8E%E6%97%A5%E4%B9%8B%E5%AD%90%E7%AC%AC%E4%BA%8C%E5%AD%A3/22476395?fromModule=lemma_inlink)》 | 担任节目厂牌星推官 [202] |
| 2017年 | 《[明日之子](/item/%E6%98%8E%E6%97%A5%E4%B9%8B%E5%AD%90/20478071?fromModule=lemma_inlink)》 | 担任该歌手养成节目首席星推官 [203] |
| 2016年 | 《[真正男子汉第二季](/item/%E7%9C%9F%E6%AD%A3%E7%94%B7%E5%AD%90%E6%B1%89%E7%AC%AC%E4%BA%8C%E5%AD%A3/17854159?fromModule=lemma_inlink)》 | 湖南卫视国防教育真人秀 [204] |

具体信息请查看节目词条

| 播出时间 | 节目名称 | 简介 |
| --- | --- | --- |
| 2025-1-24 [639] | [下班啦2024](/item/%E4%B8%8B%E7%8F%AD%E5%95%A62024/65266790?fromModule=lemma_inlink) | ---- |
| 2024-12-31 | [2024-2025湖南卫视芒果TV跨年晚会](/item/2024-2025%E6%B9%96%E5%8D%97%E5%8D%AB%E8%A7%86%E8%8A%92%E6%9E%9CTV%E8%B7%A8%E5%B9%B4%E6%99%9A%E4%BC%9A/65181640?fromModule=lemma_inlink) | 表演节目《异想记》 [636-637] |
| 2024-10-27 | 王者荣耀共创之夜 | ---- |
| 2024-10-26 | [战至巅峰第三季](/item/%E6%88%98%E8%87%B3%E5%B7%85%E5%B3%B0%E7%AC%AC%E4%B8%89%E5%AD%A3/64518926?fromModule=lemma_inlink) | 总决赛 [632] |
| 2024-10 | VOGUE盛典 [631] | ---- |
| 2024 | 百花迎春—中国文学艺术界2024春节大联欢 | 嘉宾 [596] |
| 2024 | [2024年中央广播电视总台春节联欢晚会](/item/2024%E5%B9%B4%E4%B8%AD%E5%A4%AE%E5%B9%BF%E6%92%AD%E7%94%B5%E8%A7%86%E6%80%BB%E5%8F%B0%E6%98%A5%E8%8A%82%E8%81%94%E6%AC%A2%E6%99%9A%E4%BC%9A/63593519?fromModule=lemma_inlink) | 嘉宾 [595] |
| 2024 | 2024河南春节联欢晚会 | 嘉宾 [594] |
| 2024 [620] | 2024王者荣耀共创之夜 | ---- |
| 2023 | 中央广播电视总台2023年中秋晚会 | 嘉宾 [593] |
| 2023 | [密室大逃脱第五季](/item/%E5%AF%86%E5%AE%A4%E5%A4%A7%E9%80%83%E8%84%B1%E7%AC%AC%E4%BA%94%E5%AD%A3/62615867?fromModule=lemma_inlink) | 嘉宾 [592] |
| 2023 | 2023爱奇艺尖叫之夜 | 嘉宾 [591] |
| 2022-11-30 | [红毯背后](/item/%E7%BA%A2%E6%AF%AF%E8%83%8C%E5%90%8E/62390527?fromModule=lemma_inlink) [428] | 特邀导师 |
| 2022-2-27 | [麻花特开心](/item/%E9%BA%BB%E8%8A%B1%E7%89%B9%E5%BC%80%E5%BF%83/58933545?fromModule=lemma_inlink) | 节目嘉宾 [407] |
| 2022-1-30 | 冰雪起源 | 节目嘉宾 [403] |
| 2022 | [怎么办！脱口秀专场](/item/%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%81%E8%84%B1%E5%8F%A3%E7%A7%80%E4%B8%93%E5%9C%BA/60186748?fromModule=lemma_inlink) | 节目嘉宾 [407] |
| < 上一页|1|2|3|4|下一页 >默认显示|全部显示 | | |

以上为不完全统计

费加罗 Figaro madame

2024年12月

封面

三封面 [638]

时装 LOFFICIEL

2024年10月

封面

四封面 [628]

ELLE 世界服装之苑

2024年6月

封面

三封面 [602]

marie claire 嘉人

2024年4月

封面

三封面 [627]

T magazine

2024年1月

封面

双封面 [624]

时尚 COSMOPOLITAN

2023年12月

封面

双封面 [626]

智族 GQ

2023年12月

封面

嘉人marie claire

2023年11月

封面

双封面 [447]

费加罗 Figaro madame

2023年10月 [621]

封面

ELLE 世界服装之苑

2023年8月

封面

双封面 [625]

T magazine

2023年5月

封面

费加罗男士Figaro HOMMES

2023年3月

封面

时装男士 LOFFICIEL HOMMES

2023年3月

封面

双封面 [623]

Harper's BAZAAR 时尚芭莎

2023年2月 [435]

封面

时装 LOFFICIEL

2023年1月

封面

双封面 [622]

ELLE世界时装之苑

2022年12月

封面、内页

三封面 [422]

费加罗 Figaro madame

2022年6月

封面、内页

封面人物 [410]

GLASS

2022年5月

封面、内页

封面人物 [409]

费加罗男士Figaro HOMMES

2022年5月

封面、内页

双封面 [408]

时尚 COSMOPOLITAN

2022年4月

内页、封面

主刊+电子版封面 [406]

时装男士 LOFFICIEL HOMMES

2022年3月

封面、内页

双封面 [405]

嘉人marie claire

2022年2月

封面、内页

虎年新春封面人物 [396]

时装 LOFFICIEL

2022年1月

封面、内页

开年封面人物 [395]

Harper's BAZAAR 时尚芭莎

2022年1月

封面、内页

开年封面人物 [392]

芭莎男士 BAZAAR MEN

2021年11月

封面、内页

[367]

费加罗 Figaro madame [584]

2021年8月

封面、内页

双封面

ELLE世界时装之苑 [557]

2021年8月

内页、封面

时尚先生 Esquire

2021年7月

封面

智族 GQ

2021年3月 [629]

封面

时尚 COSMOPOLITAN [571]

2021年2月

封面

时尚芭莎（越南版） [577]

2021年1月

封面

时装 LOFFICIEL [565]

2021年1月

封面

Harper's BAZAAR 时尚芭莎 [576]

2020年10月

封面

费加罗 Figaro madame [583]

2020年8月

封面

T magazine [585]

2020年7月

封面

ELLE世界时装之苑 [556]

2020年6月

封面

时尚 COSMOPOLITAN [570]

2020年5月

封面

VOGUE FILM [561]

2019年12月

封面

时装L'OFFICIEL

2019年12月

封面

中法美三国封面 [399]

ELLE世界时装之苑 [555]

2019年11月

封面

嘉人marie claire [579]

2019年8月

封面

费加罗 Figaro madame [582]

2019年6月

封面

Harper's BAZAAR 时尚芭莎 [575]

2019年3月上

封面

时尚 COSMOPOLITAN [569]

2019年1月

封面

费加罗 Figaro madame [581]

2018年8月

封面

ELLE世界时装之苑 [554]

2018年7月

封面

Harper's BAZAAR 时尚芭莎 [574]

2018年6月上

封面

时尚 COSMOPOLITAN [568]

2018年5月

封面

时装L'OFFICIEL [564]

2018年1月

封面

VOGUE Me [560]

2017年12月

封面

ELLE 世界服装之苑 [553]

2017年8月

封面

Harper's BAZAAR 时尚芭莎 [573]

2017年5月上

封面

费加罗 Figaro madame [580]

2017年4月

封面

marie claire 嘉人 [578]

2017年4月

封面

时尚 COSMOPOLITAN [567]

2017年1月

封面

ELLE 世界服装之苑 [552]

2016年11月下

封面

时装 LOFFICIEL [563]

2016年6月

封面

Vogue Collections [559]

2015年12月

封面

Harper's BAZAAR 时尚芭莎 [572]

2015年6月下

封面

ELLE 世界服装之苑 [551]

2015年4月下

封面

时尚 COSMOPOLITAN [566]

2015年3月

封面

时装 LOFFICIEL [562]

2015年2月刊

封面

VOGUE服饰与美容（别册） [558]

2015年1月

封面

ELLE 世界服装之苑 [550]

2014年2月上

封面

COSMOPOLITAN（港版） [549]

2013年4月

封面

1/9

| 播映时间 | 作品名称 | 饰演角色 | 备注信息 |
| --- | --- | --- | --- |
| 2024年 | 《[功夫熊猫4](/item/%E5%8A%9F%E5%A4%AB%E7%86%8A%E7%8C%AB4/6003348?fromModule=lemma_inlink)》 | 狐狸小真 | 动画电影 [462] |
| 2016年 | 《[捉迷藏](/item/%E6%8D%89%E8%BF%B7%E8%97%8F/19474333?fromModule=lemma_inlink)》 | 旁白 | 动画电影 [197] |
| 《[功夫熊猫3](/item/%E5%8A%9F%E5%A4%AB%E7%86%8A%E7%8C%AB3/4822795?fromModule=lemma_inlink)》 | 美美 | 动画电影 [196] |
| 2014 | 《[航海王](/item/%E8%88%AA%E6%B5%B7%E7%8E%8B/6616881?fromModule=lemma_inlink)》 | “女帝”波雅·汉库克 | 动画电影 [195] [540] |

参演短片

| 首播时间 | 作品名称 | 饰演角色 | 作品导演 | 备注信息 |
| --- | --- | --- | --- | --- |
| 2023年 | 《守路的人》 | 小⻰神 | 未知 | 王者荣耀贺岁短片 [455-456] |
| 2022年 | 《[新年快递](/item/%E6%96%B0%E5%B9%B4%E5%BF%AB%E9%80%92/49968332?fromModule=lemma_inlink)》 | - | 徐磊 | 王者荣耀贺岁短片 [401] |
| 2019年 | 《[木调灵魂](/item/%E6%9C%A8%E8%B0%83%E7%81%B5%E9%AD%82/62248170?fromModule=lemma_inlink)》 | - | 杨同坤 | VogueFilm短片 [427] |
| 2018年 | 《[心声捕手](/item/%E5%BF%83%E5%A3%B0%E6%8D%95%E6%89%8B/24206051?fromModule=lemma_inlink)》 | - | 未知 | ELLE30周年微电影 [426] |
| 《[两个小星球](/item/%E4%B8%A4%E4%B8%AA%E5%B0%8F%E6%98%9F%E7%90%83/22362266?fromModule=lemma_inlink)》 | 女孩儿 | 未知 | OPPO微电影 [425] |
| 2016年 | 《[我是你的小幂phone](/item/%E6%88%91%E6%98%AF%E4%BD%A0%E7%9A%84%E5%B0%8F%E5%B9%82phone/20277942?fromModule=lemma_inlink)》 | 小幂（[小幂phone](/item/%E5%B0%8F%E5%B9%82phone/20278737?fromModule=lemma_inlink)） | 陈正道 | OPPO微电影 [194] |
| 2015年 | 《[最美表演](/item/%E6%9C%80%E7%BE%8E%E8%A1%A8%E6%BC%94/16379334?fromModule=lemma_inlink)-囚禁》 | - | 韩延 | 新浪娱乐年终企划系列短片 [193] [379] |
| 2014年 | 《[把乐带回家2014](/item/%E6%8A%8A%E4%B9%90%E5%B8%A6%E5%9B%9E%E5%AE%B62014/14494609?fromModule=lemma_inlink)》 | 店长助理 | 韦正 | 百事贺岁微电影 |
| 2013年 | 《[把乐带回家2013](/item/%E6%8A%8A%E4%B9%90%E5%B8%A6%E5%9B%9E%E5%AE%B62013/1027390?fromModule=lemma_inlink)》 | 吵架小情侣（与韩庚） | 吴嘉洋 | 百事贺岁微电影 [191] |
| 2012年 | 《[交换旅行](/item/%E4%BA%A4%E6%8D%A2%E6%97%85%E8%A1%8C/12006067?fromModule=lemma_inlink)》 | 小幂 | 杨幂 | 导演处女作微电影 [424] |
| 《[为渴望而创](/item/%E4%B8%BA%E6%B8%B4%E6%9C%9B%E8%80%8C%E5%88%9B/7841464?fromModule=lemma_inlink)》 | 杨幂 | 韦正 | 百事微电影 [190] |
| 2011年 | 《[爱至毫厘恋上发梢](/item/%E7%88%B1%E8%87%B3%E6%AF%AB%E5%8E%98%E6%81%8B%E4%B8%8A%E5%8F%91%E6%A2%A2/2233863?fromModule=lemma_inlink)》 | Lisa | 蔡康永 | 力士微电影 [189] |
| 《[魔咒](/item/%E9%AD%94%E5%92%92/7736772?fromModule=lemma_inlink)》 | - | Eric |  |

参演短剧

| 首播时间 | 作品名称 | 饰演角色 | 作品导演 | 备注信息 |
| --- | --- | --- | --- | --- |
| 2013年 | 《[屌丝男士2](/item/%E5%B1%8C%E4%B8%9D%E7%94%B7%E5%A3%AB2/5290505?fromModule=lemma_inlink)》 | 制片人 | 大鹏 | 网络剧 [192] |
| 2011年 | 《[窈“跳”淑女](/item/%E7%AA%88%E2%80%9C%E8%B7%B3%E2%80%9D%E6%B7%91%E5%A5%B3/7018637?fromModule=lemma_inlink)》 | 扎宁 | 向灼 | 网络剧 [188] |

| 发布时间 | MV名称 | 饰演角色 | 合作歌手 |
| --- | --- | --- | --- |
| 2017年 | 《[无所事事](/item/%E6%97%A0%E6%89%80%E4%BA%8B%E4%BA%8B/21504665?fromModule=lemma_inlink)》 | 女主角 | [周笔畅](/item/%E5%91%A8%E7%AC%94%E7%95%85/129239?fromModule=lemma_inlink) [539] |
| 1993年 | 《[穿军装的川妹子](/item/%E7%A9%BF%E5%86%9B%E8%A3%85%E7%9A%84%E5%B7%9D%E5%A6%B9%E5%AD%90/7086944?fromModule=lemma_inlink)》 | 小李丹阳 | [李丹阳](/item/%E6%9D%8E%E4%B8%B9%E9%98%B3/19461?fromModule=lemma_inlink) [12] |

| 播映时间 | 作品名称 | 合作导演 | 备注信息 |
| --- | --- | --- | --- |
| 2022年 | 《荣耀时刻》 | - | 新春贺岁片幕后纪实 [402] |
| 2020年 | 《星光》 | 多名导演 | 扶贫攻坚纪录片 [388] |
| 2015年 | 《最好的我们》 | 郭敬明 | 《小时代》纪录片 [380] |

| 播映时间 | 剧目名称 | 播出平台 | 备信息注 |
| --- | --- | --- | --- |
| 2014年 | 《[微时代](/item/%E5%BE%AE%E6%97%B6%E4%BB%A3/7626967?fromModule=lemma_inlink)》 | 腾讯视频 | 首次担任制片人 [519] |

社会活动
----

播报

编辑

社会活动的基本信息

| 时间 | 备注信息 |
| --- | --- |
| 2022年 | 6月6日，杨幂参与的公益诗朗诵专辑《听·光的声音》在喜马拉雅正式上线 [413] |
| 2021年 | 1月15日，杨幂连续第三年入选北京师范大学新媒体传播研究中心、责任云研究院、封面新闻、封面新闻研究院、中国社会责任百人论坛联合发布的《中国影视明星社会责任研究报告》综合排行榜，排名分别为第72、第65和第4位； [270-272]2月，担任中国长安网主办的“平安之星网络宣传活动”的推广大使； [398]7月，为河南暴雨灾情捐款100万人民币； [366]12月29日，当选为中视协演工委执委； [393]同年，杨幂还担任了中国光华科技基金会书桥达人，并参与了关注乳腺癌防治公益活动 [404] |
| 2020年 | 2月1日，杨幂、白宇主演的《谢谢你医生》剧组通过韩红爱心慈善基金会向武汉捐款50万元，杨幂个人则捐款10万元，用于购买医疗物资为武汉及周边城市进行捐赠 [269] |
| 2019年 | 3月26日，杨幂在《中国慈善家》杂志发布的上一年度中国慈善名人榜中位列第28； [264]7月26日，其作为“星光队员”参与的《[脱贫攻坚战星光行动](/item/%E8%84%B1%E8%B4%AB%E6%94%BB%E5%9D%9A%E6%88%98%E6%98%9F%E5%85%89%E8%A1%8C%E5%8A%A8/23321594?fromModule=lemma_inlink)》在电影频道播出，节目汇报了她在前一年12月赴湖南平江完成调研工作，而杨幂也为当地的酱干等特色美食产品提出了“吃货思维”带货方式，并设计了小酱干等卡通形象； [265]12月7日，她作为“健康家庭推荐人”出席了以“健康中国，健康家庭”为主题的中国家庭健康大会，并讲述了陕西省堰河村的健康故事，向大家传递“家”与“国”之间最温暖的互动； [266]十天后，杨幂还出席了中国电影家协会行风建设培训班， [267]以及青年和新文艺群体工作委员会成立仪式，并被聘任为了副会长 [268] |
| 2018年 | 1月31日，《[中国慈善家](/item/%E4%B8%AD%E5%9B%BD%E6%85%88%E5%96%84%E5%AE%B6/2409399?fromModule=lemma_inlink)》揭晓了上一年度的中国慈善名人榜，杨幂排名第23名； [260]3月，在全国两会召开之际杨幂参与了央视电影频道推出的“脱贫攻坚战 电影人在行动”系列专题； [261]10月17日，她开始担任电影频道节目中心主办的公益项目“脱贫攻坚战——星光行动”“星光调研员”； [262]此外，杨幂还连续多年参加芭莎明星慈善夜，并参与了慈善夜的各种募捐活动 [263] |
| 2017年 | 1月16日， 杨幂在公益星榜样”慈善颁奖礼上被授予了“2016-2017年度公益星榜样”的荣誉称号， [252]并正式成为中国儿童少年基金会“爱心书箱”公益项目形象大使； [253]3月22日，她还在“世界水日”当天正式成为该年度中国妇女发展基金会-母亲水窖项目爱心大使，帮助缺水地区同胞喝上干净水，一起保护我们赖以生存的水资源； [254]随后，她还参与拍摄了由国家新闻出版广电总局电影局发起，中央电视台电影频道承制，彰显中国电影人爱国情怀的《光荣与梦想——我们的中国梦》系列公益片之“社会主义核心价值观”篇； [255]8月，杨幂与丈夫刘恺威通过中国社会福利基金会向四川九寨沟地震灾区捐款六十万元人民币； [256]9月9日，她又再次参加了芭莎明星慈善夜，并与众多艺人继续为“为爱加速”思源﹒芭莎自治区救护车项目募集善款； [257]9月24日，杨幂开始担任“中国女性宫颈健康促进计划——贝壳行动”爱心宣传大使； [258]年底，杨幂又参与了国家新闻出版广电总局，中央电视台电影频道推出的贺岁海报和公益短片《我们的新时代》的拍摄 [259] |
| 2016年 | 4月，杨幂加入壹基金大家庭，成为净水计划项目的首位爱心大使，携手壹基金关注贫困农村地区儿童的饮水安全问题； [248]4月9日，杨幂与英国奢侈品牌Aspinal of London在北京召开发布会，宣布联手打造一款慈善“杨幂包”，推出限量3000个的公益慈善款手包。每销售一款将会捐赠900元，用于支持壹基金净水计划； [249]12月12日，她还以中英电影节·英国电影季形象大使的的身份出席了电影节的开幕式； [250]此外，杨幂还连续三年担任了“暖冬行动”爱心大使，并号召社会热心人士，为偏远地区的孩子捐助御寒物资，送去温暖，与爱同行 [251] |
| 2015年 | 1月12日，杨幂在女性传媒大奖盛典上获得了年度影响力女性大奖； [242]6月15日，她还出席了《星光上海—华谊ELLE之夜》五周年庆典，并参与了现场举行的公益活动； [243]8月14日，杨幂夫妇通过中国扶贫基金平台，为天津塘沽爆炸事件捐款100万，而该款项则用来帮助爆炸事件中物资支援以及受伤民众伤患康复； [244]10月11日，她还参加了“白手杖”全国助盲公益活动，并以爱心大使的身份与学生们交流了怎样关心帮助盲人； [245]11月29日，杨幂被中国残疾人福利基金会授予“助残爱心大使”； [246]此外，她还连续三年助力爱心图书馆，并继续担任爱心图书馆公益大使 [247] |
| 2014年 | 9月28日，杨幂与海清、王宝强共同出席了关爱先天性心脏病患儿的 “酱紫一起来”社会公益活动，并呼吁更多的人关注先天性心脏病患儿； [239]12月，她参与了中英文化交流活动“伦敦国际华语电影节”并担任形象大使，6日，出席电影节颁奖典礼并被授予“海外最具影响力”奖；7日，参加在伦敦大学的海外粉丝见面会上并将见面会所得收入捐赠给母爱桥国际慈善机构；8日，参与英中影视峰会，与中英影人一起探讨中英电影的发展，并被英方授予雅典娜艺术奖—青春之星 [240-241] |
| 2013年 | 1月14日，杨幂被“[蓝丝带海洋保护协会](/item/%E8%93%9D%E4%B8%9D%E5%B8%A6%E6%B5%B7%E6%B4%8B%E4%BF%9D%E6%8A%A4%E5%8D%8F%E4%BC%9A/5962978?fromModule=lemma_inlink)授予了蓝丝带海洋公益形象大使”称号。杨幂在受聘仪式上表示她会给大家推荐分享更多有关海洋保护的知识，让更多人了解海洋环保，加入海洋生态保护的行动中； [232]4月28日，杨幂与刘恺威一同到四川，为雅安祈福，为芦山祈福。并在“中国爱·420芦山强烈地震大型公益特别节目”中以讲述人的身份在晚会最后一个篇章“希望的力量”中亮相； [233]5月，杨幂助阵垃圾分类公益环保微电影《习惯·爱》， [234]并于5月29日在微博转发了新快报官方微博内容，邀请粉丝“一起来”，参与垃圾分类； [235]7月，新浪厦门爱心图书馆转发捐助启动，而杨幂与刘恺威在第一时间便参与了微博转发， [236]并在2014年4月，与刘恺威共同担任了新浪厦门爱心图书馆的公益大使； [237]8月，杨幂加入了根与芽的“签名护鲨行动”，作为该公益活动宣传大使公开承诺不吃鱼翅，并号召公众一起保护鲨鱼，保护海洋生态 [238] |
| 2012年 | 3月26日，四川卫视中国娇子·中国爱盛典”启动仪式暨新闻发布会在北京举行。原本要出席的杨幂由于发高烧未能抵达发布会现场，但她仍然通过现场连线传达了对于公益事业的牵挂，而作为“宣传推广大使”的她还发起了“中国爱笑脸征集”活动； [230]3月，杨幂正式受邀成为了中国扶贫基金会爱心包裹项目年度爱心大使，而在前一年冬天的杨幂就已加入到了爱心包裹项目的明星阵容中；10月30日，杨幂还与阿马里·诺拉斯克共同前往医院探望美国重病儿童 [231] |
| 2011年 | 5月15日，杨幂出席了由百度百科与气候组织共同举办的“百万奇迹”线上公益活动启动仪式， [227]其在启动仪式上发出了环保倡议宣言，并被授予“百万森林爱心大使”称号； [228]10月，她还成为了“粉红丝带运动”年度代言人，并带头倡导“早预防、早发现、早治疗”乳腺癌预防的健康理念 [229] |
| 2010年 | 7月18日，杨幂参加了世界华人精英代表大会暨关中—天水经济区投资合作洽谈会”。而她则被大会授予“世界华人精英代表大会”的首批形象大使并获发了荣誉证书；9月，她还被中国儿童基金会授予了爱心大使奖杯 [226] |

杨幂参加活动图册

获奖记录
----

播报

编辑

|  |
| --- |
| 其他 |
| | 获奖时间 | 奖项名称 | 获奖结果 | | --- | --- | --- | | 2024-10-19 | VOGUE时尚之力盛会#Force of Fashion Award时尚之力大奖“年度潮流引领者奖” [635] | 获奖 | | 2023-12-7 | 智族GQ MOTY年度人物盛典年度艺人 [450] | 获奖 | | 2021-2-28 | 微博年度之星 [273] | 获奖 | | 2021-1-10 | 腾讯娱乐白皮书年度之星 [274] | 获奖 | | 2021-1-10 | 腾讯娱乐白皮书年度影响力和商业价值女明星 [404] | 获奖 | | 2020-12-10 | 第17届MAHB年度先生盛典年度最美丽女人 [275] | 获奖 | | 2020-12-2 | COSMO时尚盛典“时尚无惧”年度人物 [277] | 获奖 | | 2020-6-22 | TCCAsia中国百大最具“颜响力”面孔第二十一位 [597] | 提名 | | 2025-1 | 2024中国银幕风云榜年度风尚 [641] | 获奖 | |
| 社会类 |
| | 获奖时间 | 奖项名称 | 获奖结果 | | --- | --- | --- | | 2024-1-13 | [2023微博之夜](/item/2023%E5%BE%AE%E5%8D%9A%E4%B9%8B%E5%A4%9C/63924148?fromModule=lemma_inlink)微博星光公益人物 [453] | 获奖 | | 2021-8-20 | 中国福布斯名人榜第4名 [364] | 获奖 | | 2020-12-8 | 福布斯亚洲百大数字之星 [276] | 提名 | | 2020-12-1 | 行动者联盟公益盛典年度十大公益人物 [278] | 获奖 | | 2020 | 福布斯中国名人榜第6名 [87] | 获奖 | | 2019 | 福布斯中国名人榜第9名 [83] | 获奖 | | 2017-09-22 | 福布斯中国名人榜第3位 [302] | 获奖 | | 2013 | 福布斯中国名人榜第7名 [521] | 获奖 | | 2012 | 福布斯中国名人榜第13名 [515] | 获奖 | | 2011 | 福布斯中国名人榜第92名 [510] [515] | 获奖 | | 2007-04-12 | 福布斯中国名人颁奖盛典最具潜力名人奖 [348] | 获奖 | |
| 影视类 |
| | 获奖时间 | 奖项名称 | 获奖作品 | 获奖结果 | | --- | --- | --- | --- | | 2023-11-25 | 爱奇艺“尖叫之夜”2024观众瞩目女演员 [448] |  | 获奖 | | 2023-3-25 | 微博之夜年度质感演员 [436] |  | 获奖 | | 2021-11-15 | 第18届广州大学生电影展年度女主角 [370] | [刺杀小说家](/item/%E5%88%BA%E6%9D%80%E5%B0%8F%E8%AF%B4%E5%AE%B6/19776773?fromModule=lemma_inlink) | 提名 | | 2020-12 | 腾讯视频星光大赏年度VIP之星 [279] |  | 获奖 | | 2020-12 | 腾讯视频星光大赏年度最具商业价值艺人 [279] |  | 获奖 | | 2020-9 | [第30届中国电视金鹰奖](/item/%E7%AC%AC30%E5%B1%8A%E4%B8%AD%E5%9B%BD%E7%94%B5%E8%A7%86%E9%87%91%E9%B9%B0%E5%A5%96/50066630?fromModule=lemma_inlink)观众喜爱的女演员奖 [451] | [扶摇](/item/%E6%89%B6%E6%91%87/20216615?fromModule=lemma_inlink) | 提名 | | 2016-11 | [第16届华语电影传媒大奖](/item/%E7%AC%AC16%E5%B1%8A%E5%8D%8E%E8%AF%AD%E7%94%B5%E5%BD%B1%E4%BC%A0%E5%AA%92%E5%A4%A7%E5%A5%96/19584189?fromModule=lemma_inlink)最受瞩目女演员 [360] | [我是证人](/item/%E6%88%91%E6%98%AF%E8%AF%81%E4%BA%BA/16785929?fromModule=lemma_inlink) | 提名 | | 2011-10 | 第2届中国大学生电视节最受大学生喜爱电视剧女演员 [359] | 宫锁心玉 | 提名 | | 2010-10 | 第1届中国大学生电视节最受大学生喜爱电视剧女演员 | 仙剑奇侠传三 | 提名 | |
| 综合奖项 |
| | 获奖时间 | 奖项名称 | 获奖作品 | 获奖结果 | | --- | --- | --- | --- | | 2020-01-12 | 第1届[融屏传播年度优选](/item/%E8%9E%8D%E5%B1%8F%E4%BC%A0%E6%92%AD%E5%B9%B4%E5%BA%A6%E4%BC%98%E9%80%89/24434125?fromModule=lemma_inlink)“影响力演员” [280] |  | 获奖 | | 2018-12-18 | 腾讯视频星光盛典年度电视剧女演员 [287] |  | 获奖 | | 2017-12-28 | 腾讯娱乐白皮书年度之星 [294] |  | 获奖 | | 2017-12-21 | 第6届搜狐时尚盛典年度电视剧网络剧女明星 [295] |  | 获奖 | | 2017-12-21 | 第6届搜狐时尚盛典年度人气女明星 [295] |  | 获奖 | | 2017-12-03 | 腾讯视频星光大赏年度VIP之星 [297] |  | 获奖 | | 2017-12-03 | 腾讯视频星光大赏年度综艺之星 [298] |  | 获奖 | | 2017-12-02 | 爱奇艺尖叫之夜年度戏剧女艺人 [299] |  | 获奖 | | 2017-04-25 | 最具粉丝影响力明星颁奖盛典最具实力女艺人奖 [306] |  | 获奖 | | 2016-10-30 | 时装之夜年度盛典最受欢迎演员 [309] |  | 获奖 | | 2015-11-03 | 2015亚洲影响力年度电影力量 [311] |  | 获奖 | | 2015-03-06 | 第8届金芒果电视星光大赏年度女演员 |  | 获奖 | | 2014-12-12 | 第6届中国时尚权力榜年度最佳演员 [316] |  | 获奖 | | 2014-12-06 | [第3届伦敦国际华语电影节](/item/%E7%AC%AC3%E5%B1%8A%E4%BC%A6%E6%95%A6%E5%9B%BD%E9%99%85%E5%8D%8E%E8%AF%AD%E7%94%B5%E5%BD%B1%E8%8A%82/17353407?fromModule=lemma_inlink)“最具海外影响力演员” [317] |  | 获奖 | | 2012-12-31 | 国剧盛典“年度网络最受欢迎全能艺人(内地)” [321] |  | 获奖 | | 2012-01-11 | 搜狐视频电视剧盛典“最具网络人气女演员” [329] |  | 获奖 | | 2012-01-05 | 《精品购物指南》中国影响2011· 时尚盛典“年度电视剧女主角” [330] |  | 获奖 | | 2012-01-05 | 《精品购物指南》中国影响2011· 时尚盛典“年度风云人物” [330] |  | 获奖 | | 2011-12-31 | 国剧盛典“年度最具人气演员” [333] |  | 获奖 | | 2011-12-05 | 北京电视台文娱十年影响力盛典“最佳新秀人气奖” [334] |  | 获奖 | | 2011-10-25 | 新势力盛典“最受欢迎电影女演员” [336] | 孤岛惊魂 | 获奖 | | 2011-08-26 | 乐视影视盛典“亚太地区最具人气演员” [337] |  | 获奖 | | 2011-08-19 | 风尚权力榜“年度风尚最具人气女演员” [338] |  | 获奖 | | 2011-06-25 | 第4届中国网络影响力2010年十大影视演员 | 宫锁心玉 | 获奖 | | 2011-04-15 | 第15届全球华语音乐榜中榜暨亚洲影响力大典“最佳电视剧女演员(内地)” [340] |  | 获奖 | | 2011-03-31 | 第5届娱乐大典“特别关注飞跃人物(电视剧类)” [341] | 宫锁心玉 | 获奖 | | 2011-03-28 | MSN时尚夜暨星月对话两周年颁奖典礼“MSN星月风尚当红明星” [342] |  | 获奖 | | 2011-03-18 | 东方影视盛典“电视剧年度最具人气价值女演员” [343] |  | 获奖 | | 2011-03-01 | 优酷影视指数盛典“开年人气女演员奖” [344] | 宫锁心玉 | 获奖 | | 2010-12-31 | 风尚盛典“年度风尚新人” [345] |  | 获奖 | | 2010-04-26 | 春季电视剧互联网盛典“最具网络生命力电视剧top5” [346] | 仙剑奇侠传三 | 获奖 | | 2007-06-08 | 第3届电视剧风云榜最佳新人奖 [347] | 神雕侠侣 | 提名 | | 2006-12-30 | 第3届中国影视星锐榜年度十佳 [349] |  | 获奖 | |
| 微博之夜 |
| | 获奖时间 | 奖项名称 | 获奖结果 | | --- | --- | --- | | 2020-01-11 | 2019新浪微博之夜星光公益影响力人物 [281] | 获奖 | | 2020-01-11 | 2019新浪微博之夜微博年度女神 [282] | 获奖 | | 2018-01-18 | 2017新浪“微博之夜”网络盛典“微博Queen” [292] | 获奖 | | 2017-06-18 | 第2届新浪微博电影之夜最受期待演员 [303] | 获奖 | | 2015-01-15 | 2014新浪“微博之夜”网络盛典“微博年度突破力” [51] | 获奖 | | 2012-01-04 | 2011新浪“微博之夜”网络盛典“微博Queen” [331] | 获奖 | | 2012-01-04 | 2011新浪“微博之夜”网络盛典“最具影响力电视剧女演员” [332] | 获奖 | |
| 大学生电影节 |
| | 获奖时间 | 奖项名称 | 获奖作品 | 获奖结果 | | --- | --- | --- | --- | | 2019-12 | 第16届[广州大学生电影节](/item/%E5%B9%BF%E5%B7%9E%E5%A4%A7%E5%AD%A6%E7%94%9F%E7%94%B5%E5%BD%B1%E8%8A%82/6979108?fromModule=lemma_inlink)最受大学生欢迎女主角奖 [283] | [宝贝儿](/item/%E5%AE%9D%E8%B4%9D%E5%84%BF/22291142?fromModule=lemma_inlink) | 获奖 | | 2018-05 | [第25届北京大学生电影节](/item/%E7%AC%AC25%E5%B1%8A%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6%E7%94%9F%E7%94%B5%E5%BD%B1%E8%8A%82/22412803?fromModule=lemma_inlink)最受大学生欢迎女演员奖 [3] | [绣春刀2：修罗战场](/item/%E7%BB%A3%E6%98%A5%E5%88%802%EF%BC%9A%E4%BF%AE%E7%BD%97%E6%88%98%E5%9C%BA/20396936?fromModule=lemma_inlink) | 获奖 | |
| 评选奖项 |
| | 获奖时间 | 奖项名称 | 获奖结果 | | --- | --- | --- | | 2019-11-09 | TCCAsia2019年度亚太百大最美面孔第20位 [284] | 提名 | | 2019-03-17 | TCCAsia中国百大最美面孔第11位 [285] | 提名 | | 2019-03-16 | TCCAsia2018年度亚太百大最美面孔第22位 [286] | 提名 | | 2018-04-12 | 世界最受尊敬女性排名第17位 [291] | 提名 | |
| 时尚奖项 |
| | 获奖时间 | 奖项名称 | 获奖结果 | | --- | --- | --- | | 2018-12-04 | 第15届MAHB年度先生盛典年度最受欢迎女艺人 [288] | 获奖 | | 2018-11-28 | COSMO时尚美丽盛典年度闪耀美丽偶像 [289] | 获奖 | | 2017-12-18 | COSMO时尚美丽盛典年度最美人物 [296] | 获奖 | | 2016-11-08 | COSMO时尚美丽盛典年度年度最具影响力偶像 [308] | 获奖 | | 2012-12-21 | 红秀GRAZIA潮流影响力颁奖礼“年度潮流魅惑力奖” [322] | 获奖 | |
| 中国电视好演员奖 |
| | 获奖时间 | 奖项名称 | 获奖结果 | | --- | --- | --- | | 2018-12 | [第五届中国电视好演员奖](/item/%E7%AC%AC%E4%BA%94%E5%B1%8A%E4%B8%AD%E5%9B%BD%E7%94%B5%E8%A7%86%E5%A5%BD%E6%BC%94%E5%91%98%E5%A5%96/56467070?fromModule=lemma_inlink)绿宝石女演员奖 [4] | 获奖 | | 2018-10 | [第五届中国电视好演员奖](/item/%E7%AC%AC%E4%BA%94%E5%B1%8A%E4%B8%AD%E5%9B%BD%E7%94%B5%E8%A7%86%E5%A5%BD%E6%BC%94%E5%91%98%E5%A5%96/56467070?fromModule=lemma_inlink)优秀演员奖 [4] | 获奖 | | 2016-10 | 第3届[中国电视好演员奖](/item/%E4%B8%AD%E5%9B%BD%E7%94%B5%E8%A7%86%E5%A5%BD%E6%BC%94%E5%91%98%E5%A5%96/24133630?fromModule=lemma_inlink)绿宝石女演员奖提名/优秀演员奖 [310] | 获奖 | | 2015-09 | 第2届[中国电视好演员奖](/item/%E4%B8%AD%E5%9B%BD%E7%94%B5%E8%A7%86%E5%A5%BD%E6%BC%94%E5%91%98%E5%A5%96/24133630?fromModule=lemma_inlink)绿宝石女演员奖提名/优秀演员奖 [313] | 获奖 | | 2014-03 | 第1届中国电视好演员奖行业形象金榜 [318] | 获奖 | |
| 华鼎奖 |
| | 获奖时间 | 奖项名称 | 获奖作品 | 获奖结果 | | --- | --- | --- | --- | | 2018-10 | [第24届华鼎奖](/item/%E7%AC%AC24%E5%B1%8A%E5%8D%8E%E9%BC%8E%E5%A5%96/22877769?fromModule=lemma_inlink)中国古装题材电视剧最佳女演员 [290] | [扶摇](/item/%E6%89%B6%E6%91%87/20216615?fromModule=lemma_inlink) | 提名 | | 2015-08 | [第17届华鼎奖](/item/%E7%AC%AC17%E5%B1%8A%E5%8D%8E%E9%BC%8E%E5%A5%96/0?fromModule=lemma_inlink)中国百强电视剧最佳女演员奖 [314] | [古剑奇谭](/item/%E5%8F%A4%E5%89%91%E5%A5%87%E8%B0%AD/5016869?fromModule=lemma_inlink) | 提名 | | 2012-11 | 第8届[华鼎奖](/item/%E5%8D%8E%E9%BC%8E%E5%A5%96/0?fromModule=lemma_inlink)中国百强电视剧最佳女主角奖 [324] | [如意](/item/%E5%A6%82%E6%84%8F/254841?fromModule=lemma_inlink) | 提名 | | 2012-11 | 第8届华鼎奖中国传奇题材电视剧最佳女演员奖 [324] | [唐宫美人天下](/item/%E5%94%90%E5%AE%AB%E7%BE%8E%E4%BA%BA%E5%A4%A9%E4%B8%8B/5798169?fromModule=lemma_inlink) | 提名 | | 2012-11 | 第8届华鼎奖全国观众最喜爱的影视明星奖 [324] |  | 提名 | | 2011-12 | [第6届华鼎奖](/item/%E7%AC%AC6%E5%B1%8A%E5%8D%8E%E9%BC%8E%E5%A5%96/20706016?fromModule=lemma_inlink)百强电视剧最佳主题曲演唱奖 [335] | 宫锁心玉 | 获奖 | |
| 公益奖项 |
| | 获奖时间 | 奖项名称 | 获奖结果 | | --- | --- | --- | | 2018-01-11 | 中国社会福利基金会年度爱心个人奖 [293] | 获奖 | | 2015-01-12 | 第5届女性传媒大奖“年度影响力女性” [315] | 获奖 | | 2013-03-20 | 第3届“明星公民暨金牌推手”颁奖盛典“年度明星公民” [320] | 获奖 | |
| 国际影视节奖项 |
| | 获奖时间 | 奖项名称 | 获奖作品 | 获奖结果 | | --- | --- | --- | --- | | 2017-12 | [第1届塞班国际电影节](/item/%E7%AC%AC1%E5%B1%8A%E5%A1%9E%E7%8F%AD%E5%9B%BD%E9%99%85%E7%94%B5%E5%BD%B1%E8%8A%82/0?fromModule=lemma_inlink)最佳女主角奖 [300] | [绣春刀Ⅱ：修罗战场](/item/%E7%BB%A3%E6%98%A5%E5%88%80%E2%85%A1%EF%BC%9A%E4%BF%AE%E7%BD%97%E6%88%98%E5%9C%BA/20393681?fromModule=lemma_inlink) | 提名 | | 2017-12 | [第8届澳门国际电视节](/item/%E7%AC%AC8%E5%B1%8A%E6%BE%B3%E9%97%A8%E5%9B%BD%E9%99%85%E7%94%B5%E8%A7%86%E8%8A%82/0?fromModule=lemma_inlink)最佳女演员奖 [301] | [三生三世十里桃花](/item/%E4%B8%89%E7%94%9F%E4%B8%89%E4%B8%96%E5%8D%81%E9%87%8C%E6%A1%83%E8%8A%B1/16246274?fromModule=lemma_inlink) | 提名 | | 2017-06 | 第3届[成龙动作电影周](/item/%E6%88%90%E9%BE%99%E5%8A%A8%E4%BD%9C%E7%94%B5%E5%BD%B1%E5%91%A8/0?fromModule=lemma_inlink)-[钢铁人奖](/item/%E9%92%A2%E9%93%81%E4%BA%BA%E5%A5%96/0?fromModule=lemma_inlink)最佳动作片女演员奖 [304] | [逆时营救](/item/%E9%80%86%E6%97%B6%E8%90%A5%E6%95%91/20601217?fromModule=lemma_inlink) | 获奖 | | 2017-06 | [第20届上海国际电影节](/item/%E7%AC%AC20%E5%B1%8A%E4%B8%8A%E6%B5%B7%E5%9B%BD%E9%99%85%E7%94%B5%E5%BD%B1%E8%8A%82/0?fromModule=lemma_inlink)-[电影频道传媒大奖](/item/%E7%94%B5%E5%BD%B1%E9%A2%91%E9%81%93%E4%BC%A0%E5%AA%92%E5%A4%A7%E5%A5%96/0?fromModule=lemma_inlink)最受关注女主角奖 [305] | 逆时营救 | 提名 | | 2017-04 | 第50届[休斯敦国际电影节](/item/%E4%BC%91%E6%96%AF%E6%95%A6%E5%9B%BD%E9%99%85%E7%94%B5%E5%BD%B1%E8%8A%82/2930483?fromModule=lemma_inlink)最佳女主角奖 [307] | 逆时营救 | 获奖 | |
| 华语电影传媒大奖 |
| | 获奖时间 | 奖项名称 | 获奖作品 | 获奖结果 | | --- | --- | --- | --- | | 2015-10 | [第15届华语电影传媒大奖](/item/%E7%AC%AC15%E5%B1%8A%E5%8D%8E%E8%AF%AD%E7%94%B5%E5%BD%B1%E4%BC%A0%E5%AA%92%E5%A4%A7%E5%A5%96/0?fromModule=lemma_inlink)最受瞩目女演员奖 [312] | [小时代3：刺金时代](/item/%E5%B0%8F%E6%97%B6%E4%BB%A33%EF%BC%9A%E5%88%BA%E9%87%91%E6%97%B6%E4%BB%A3/12702233?fromModule=lemma_inlink) | 提名 | | 2013-08 | [第13届华语电影传媒大奖](/item/%E7%AC%AC13%E5%B1%8A%E5%8D%8E%E8%AF%AD%E7%94%B5%E5%BD%B1%E4%BC%A0%E5%AA%92%E5%A4%A7%E5%A5%96/0?fromModule=lemma_inlink)最受瞩目女演员 [319] | 春娇与志明 | 提名 | | 2012-05 | [第12届华语电影传媒大奖](/item/%E7%AC%AC12%E5%B1%8A%E5%8D%8E%E8%AF%AD%E7%94%B5%E5%BD%B1%E4%BC%A0%E5%AA%92%E5%A4%A7%E5%A5%96/0?fromModule=lemma_inlink)观众票选最受瞩目表现 [326] | [孤岛惊魂](/item/%E5%AD%A4%E5%B2%9B%E6%83%8A%E9%AD%82/8060879?fromModule=lemma_inlink) | 提名 | |
| 音乐奖项 |
| | 获奖时间 | 奖项名称 | 获奖作品 | 获奖结果 | | --- | --- | --- | --- | | 2012-12-08 | 第6届中国移动无线音乐盛典咪咕汇“年度最畅销影视剧金曲奖” [323] | 爱的供养 | 获奖 | | 2012-08-21 | 第11届[CCTV-MTV音乐盛典](/item/CCTV-MTV%E9%9F%B3%E4%B9%90%E7%9B%9B%E5%85%B8/0?fromModule=lemma_inlink)“内地年度最受欢迎女歌手” [325] |  | 获奖 | | 2012-04-13 | 第11届[全球华语榜中榜](/item/%E5%85%A8%E7%90%83%E5%8D%8E%E8%AF%AD%E6%A6%9C%E4%B8%AD%E6%A6%9C/0?fromModule=lemma_inlink)“内地最佳跨界歌手” [327] |  | 获奖 | | 2012-01-19 | [中歌榜](/item/%E4%B8%AD%E6%AD%8C%E6%A6%9C/0?fromModule=lemma_inlink)2011年度北京流行音乐典礼“年度最受欢迎新人(女)” [328] |  | 获奖 | |
| 中国电视金鹰奖 |
| | 获奖时间 | 奖项名称 | 获奖作品 | 获奖结果 | | --- | --- | --- | --- | | 2012-09 | [第9届中国金鹰电视艺术节](/item/%E7%AC%AC9%E5%B1%8A%E4%B8%AD%E5%9B%BD%E9%87%91%E9%B9%B0%E7%94%B5%E8%A7%86%E8%89%BA%E6%9C%AF%E8%8A%82/0?fromModule=lemma_inlink)最具人气女演员奖 [41] | [北京爱情故事](/item/%E5%8C%97%E4%BA%AC%E7%88%B1%E6%83%85%E6%95%85%E4%BA%8B/28263?fromModule=lemma_inlink) | 获奖 | | 2012-09 | [第26届中国电视金鹰奖](/item/%E7%AC%AC26%E5%B1%8A%E4%B8%AD%E5%9B%BD%E7%94%B5%E8%A7%86%E9%87%91%E9%B9%B0%E5%A5%96/0?fromModule=lemma_inlink)观众喜爱的电视剧女演员奖 [442] | [北京爱情故事](/item/%E5%8C%97%E4%BA%AC%E7%88%B1%E6%83%85%E6%95%85%E4%BA%8B/28263?fromModule=lemma_inlink) | 提名 | | 2008-08 | [第24届中国电视金鹰奖](/item/%E7%AC%AC24%E5%B1%8A%E4%B8%AD%E5%9B%BD%E7%94%B5%E8%A7%86%E9%87%91%E9%B9%B0%E5%A5%96/0?fromModule=lemma_inlink)观众喜爱的电视剧女演员奖 [441] | [王昭君](/item/%E7%8E%8B%E6%98%AD%E5%90%9B/4424411?fromModule=lemma_inlink) | 提名 | |
| 上海电视节-白玉兰奖 |
| | 获奖时间 | 奖项名称 | 获奖作品 | 获奖结果 | | --- | --- | --- | --- | | 2011-06 | [第17届上海电视节](/item/%E7%AC%AC17%E5%B1%8A%E4%B8%8A%E6%B5%B7%E7%94%B5%E8%A7%86%E8%8A%82/0?fromModule=lemma_inlink)-[白玉兰奖](/item/%E7%99%BD%E7%8E%89%E5%85%B0%E5%A5%96/11447?fromModule=lemma_inlink)最具人气女演员奖 | 宫锁心玉 | 获奖 | | 2011-06 | [第17届上海电视节](/item/%E7%AC%AC17%E5%B1%8A%E4%B8%8A%E6%B5%B7%E7%94%B5%E8%A7%86%E8%8A%82/0?fromModule=lemma_inlink)-[白玉兰奖](/item/%E7%99%BD%E7%8E%89%E5%85%B0%E5%A5%96/11447?fromModule=lemma_inlink)最佳女演员奖 [339] | 宫锁心玉 | 提名 | |

争议事件
----

播报

编辑

2023年1月，因泉州童龄纺贸易有限公司以“杨幂”为关键词在涉案店铺内检索出38条商品链接，未经杨幂许可，在其经营的店铺中使用原告肖像用于广告宣传，出于营利目的吸引公众关注、购买商品，构成了对杨幂肖像权的侵犯，事后未履行致歉义务，杨幂申请强制执行，北京互联网法院公告杨幂与该公司网络侵权责任纠纷一案判决书主要内容 [598]。

公告显示，被告系涉案店铺运营主体，以“杨幂”为关键词在涉案店铺内检索出38条商品链接。被告未经原告杨幂许可，在其经营的店铺中使用原告肖像用于广告宣传，出于营利目的吸引公众关注、购买商品，已经构成了对原告肖像权的侵犯。法院判决被告在其经营的店铺向杨幂赔礼道歉，赔偿杨幂经济损失及取证费共计18470元 [598]。

2004年6月29日，记者从天涯社区上看到一篇名为《张纪中的郭襄找到了》的帖子，但是，她在中国某知名论坛上被称为“小太妹”，并贴出多张她对着镜头竖起中指的照片。而在2005年3月的采访中，杨幂则对自己当年不成熟的行为表达了后悔的意思 [354] [444]。

2024年10月14日，北京互联网法院向刘某某公告送达杨幂与其网络侵权责任纠纷案件起诉状副本及开庭传票等，该案将于12月3日开庭审理。 [630]

2015年10月21日，杨幂在影片《我是证人》的成都发布会上承诺为成都市特殊教育学校的盲人学生捐献100根盲杖、50台盲人打字机 [355]。但是，一直到2018年3月该承诺始终没有兑现。一时间，杨幂陷入“诈捐门”事件。实际上，这次捐赠的关键人物李萌并非杨幂工作室人员，在整个捐赠中，他的身份始终是“中间人”。由于李萌并未及时处理这次的捐赠事宜，因此捐赠就被搁置一旁 [355-356]。3月30日，杨幂方面在经过一系列的运作和协调后，终于完成了全部捐赠物资的采购工作 [355]。此后，杨幂方面与李萌开始了合法权益的诉讼 [445]。

2019年3月20日，北京西城区法院对李萌诉杨幂方名誉侵权案发布一审民事判决书。判决书显示不能认定杨幂方构成对李萌名誉权的侵犯。法院驳回原告李萌的全部诉讼请求，李萌败诉，杨幂胜诉 [357]。

人物评价
----

播报

编辑

杨幂外形漂亮可爱、同时又天生带点儿北京女孩大而化之的豪气，作为85后美女的她一直在影视行业勤劳耕耘，如同杨幂粉丝的称号“蜜蜂”，“蜂王”杨幂自涉足影视便兢兢业业、不畏劳苦，无论角色大小，杨幂的表演都会给观众留下深刻的印象。比如在《神雕侠侣》中出演此剧的点睛之笔“小东邪”郭襄一角。杨幂的表演细腻到位，并获得了更多观众的认可。（新浪娱乐 评 [350]）

2014年俨然成了杨幂展示自己市场号召力的秀场，她以多部作品共30亿的票房总数位居女演员之首，仅在暑期档杨幂便凭借《分手大师》《小时代3》成为身拥10亿票房的电影女主角。在电视和网络上，杨幂也不断发力，她主演的《古剑奇谭》虽为周播剧，每逢播出却必拿当日收视第一，其首当制片人的《微时代》也以4天破4000万的点击量备受关注，而她之前主演的《仙剑奇侠传3》《宫锁心玉》等作品则被从卫视到地方台轮番播出且收视率不俗，一时之间“杨幂效应”已然形成。（新浪娱乐 评 [351-352]）

杨幂在电视剧《亲爱的翻译官》中，尽显其市场号召力，而除了号召力，她更是用实力说话，饰演的吃土宝宝乔菲倔强励志，富有感染力。从《亲爱的翻译官》的播出数据来看，杨幂的“收视副将”之称名不虚传，作为她生子之后睽违两年的电视荧屏回归之作，该剧从开拍到开播，一直备受关注，其意料之中又不失惊喜的收视成绩，也显示了她一直以来的强大号召力。而从《宫1》《如意》《古剑奇谭》再到《亲爱的翻译官》，杨幂都证明了她是当之无愧的收视冠军剧女主角。（凤凰娱乐 评 [353]）

Process finished with exit code 0

    """
