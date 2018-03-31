"""
项目2----豆瓣上最好的【电影】

任务1:获取每个【地区】、每个【类型】页面的URL

分解 URL 可以看到其中包含:

https://movie.douban.com/tag/#/: 豆瓣电影分类页面
sort=S: 按评分排序
range=9,10: 评分范围 9 ~ 10
tags=电影: 标签为电影

其中参数tags可以包含多个以逗号分隔的标签，
你可以分别选取类型和地区来进行进一步的筛选，
例如选择【类型】为剧情，【地区】为美国,
那么 URL 为https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,剧情,美国

实现函数构造对应【类型】和【地区】的【URL地址】
"""

def getMovieUrl(category, location):
	"""
	return a string corresponding to
	the URL of douban movie lists
	given category and location.
	"""
	url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}".format(category, location)
	return url
#print(getMovieUrl("movie", "China"))



"""
任务2: 获取电影页面 HTML

获得URL后，我们可以获取 URL 【对应页面的 HTML】

在课程中，我们使用库 requests get 函数。

import requests
response = requests.get(url)
html = response.text

这样的做法对大多数豆瓣电影列表页面来说没什么问题。但有些列表需要【多页显示】，
我们需要【不断模拟点击】【加载更多】按钮来显示这个列表上的全部电影。

这个任务虽然不难，但并不是课程的重点。因此我们已经为你完成了这个任务。
你只需要导入我们已经写好的文件，并调用库就可以了

要使用这个写好的函数，你需要在windows【安装】 selenium 和 chromedriver

getHtml 还有【两个可选参数:多页，翻页等待时间】，你 【很有可能】 需要传入非默认的值。

def getMovieDetails(url, category, location):
	html = expanddouban.getHtml(url, True, 3)#获取html
	soup = BeautifulSoup(html)#将html变为可以解析的soup对象

	#获取父元素，class必须加下划线
	parent_a = soup.find("div", class_="list-wp").find_all("a", class_="item")
	for child in parent_a:
		name = child.find(span, class_="title").string
		rate = child.find(span, class_="rate").string
		info_link = child.get('href')#找到链接，见BeautifulSoup“从文档中找到所有<a>标签的链接”
		cover_link = child.find('img').get('src')
		m = Movie(name, rate, location, category, info_link, cover_link)
		movieList.append(m)

	return

"""
# for test
#url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,剧情,美国"
#html = expanddouban.getHtml(url)
##print(html)

import expanddouban
from bs4 import BeautifulSoup

"""
任务3: 定义电影类

电影类应该【包含】以下成员【变量】

电影名称
电影评分
电影类型
电影地区
电影页面链接
电影海报图片链接
同时，你应该实现电影类的【构造函数】。

name = “肖申克的救赎”
rate = 9.6
location = "美国"
category = "剧情"
info_link = "https://movie.douban.com/subject/1292052/"【页面链接】
cover_link = “https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p480747492.jpg”【海报图片链接】

m = Movie(name, rate, location, category, info_link, cover_link)
"""
class Movie(object):

    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

    def print_movie(self):
        return "{},{},{},{},{},{}".format(self.name,self.rate,self.location,self.category,self.info_link,self.cover_link)#如果没有这个方法，Movie的每个实例输出为<__main__.Movie object at 0x05977410>

"""
任务4: 获得豆瓣电影的信息

通过URL返回的【HTML】，我们可以获取网页中所有电影的【名称】，【评分】，【海报图片链接】和【页面链接】，
同时我们在任务1构造【URL】时，也有【类型】和【地区】的信息，
因为我们可以完整的构造每一个电影，并得到一个列表。

提示：你可能需要在这个任务中，使用前三个任务的代码或函数。
"""
#一个类型+一个地区
def getMovies(category, location):
	"""
	return a list of Movie objects with a given category and location.
	"""
	url = getMovieUrl(category, location)
	html = expanddouban.getHtml(url, True, 3)#获取html
	soup = BeautifulSoup(html, "html.parser")#将html变为可以解析的soup对象

	movieList = []

	#获取父元素，class必须加下划线
	parent_a = soup.find('div', class_="list-wp").find_all("a", class_="item")
	for child in parent_a:
		#从html中获取名称、评分等信息
		name = child.find('span', class_="title").string
		rate = child.find('span', class_="rate").string
		info_link = child.get('href')#找到链接，见BeautifulSoup“从文档中找到所有<a>标签的链接”
		cover_link = child.find('img').get('src')

		#建立新实例，并添加到list
		m = Movie(name, rate, location, category, info_link, cover_link).print_movie()
		movieList.append(m)

	return movieList
#print(getMovies('爱情', '大陆'))

#多个类型 + 多个地区
def getAllMovies(categories, locations):
	"""
	return a list of Movie objects with a list of given categories and locations.
	"""
	allMovies = []
	for category in categories:
		for location in locations:
			#allMovies.append(getMovies(category, location))
			print(getMovies(category, location))
			print(getMovies('爱情', '大陆'))
			print(category)
			print(location)

			#print(allMovies)
	return sum(allMovies, [])

"""
任务5: 构造电影信息数据表

从网页上选取你最爱的三个电影类型，然后获取每个地区的电影信息后，
我们可以获得一个包含【三个类型】、【所有地区】，【评分超过9分】的完整电影对象的列表。
将列表【输出到文件】 【movies.csv】，格式如下:

肖申克的救赎,9.6,美国,剧情,https://movie.douban.com/subject/1292052/,https://img3.doubanio.com/p480747492.jpg
霍伊特团队,9.0,香港,动作,https://movie.douban.com/subject/1307914/,https://img3.doubanio.com/p2329853674.jpg

去除重复？


"""
myMovies = getAllMovies(['爱情'], ['全部地区'])

#print(myMovies)
"""
任务6: 统计电影数据

统计你所选取的【每个电影类别】中，数量排名【前三】的【地区】有哪些，分别占此类别电影总数的【百分比】为多少？

你可能需要自己把这个任务拆分成多个步骤，统计每个类别的电影个数，统计每个类别每个地区的电影个数，排序找到最大值，做一定的数学运算等等，相信你一定可以的！

请将你的结果【输出文件】 【output.txt】
"""

"""
请提交submit.zip, 包含以下文件：

DoubanCrawler.py
movies.csv
output.txt

不要提交其他任何文件

注意运行 python 【DoubanCrawler.py】 后，脚本应该会在同一个文件夹【生成】 movies.csv 和 output.txt 两个文件。
"""
