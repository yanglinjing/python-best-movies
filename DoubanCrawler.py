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
import expanddouban
from bs4 import BeautifulSoup
import csv
import codecs

def getMovieUrl(category, location):
	"""
	return a string corresponding to
	the URL of douban movie lists
	given category and location.
	rate >=9
	"""
	url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}".format(category, location)
	return url

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

"""
# for test
#url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,剧情,美国"
#html = expanddouban.getHtml(url)
##print(html)

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

	def getOneMovie(self):
		return self.name, self.rate, self.location, self.category, self.info_link, self.cover_link
		#如果没有这个方法，Movie的每个实例输出为<__main__.Movie object at 0x05977410>


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

		#建立新实例，用getOneMovie方法变成tuple，并添加到list
		m = Movie(name, rate, location, category, info_link, cover_link).getOneMovie()
		movieList.append(m)

	return movieList


#多个类型 + 多个地区
def getAllMovies(categories, locations):
	"""
	return a list of Movie objects with a list of given categories and locations.
	"""
	movieList = []
	for category in categories:
		for location in locations:
			movieList.append(getMovies(category, location))
	return sum(movieList, [])

"""
任务5: 构造电影信息数据表

从网页上选取你最爱的三个电影类型，然后获取每个地区的电影信息后，
我们可以获得一个包含【三个类型】、【所有地区】，【评分超过9分】的完整电影对象的列表。
将列表【输出到文件】 【movies.csv】，格式如下:

肖申克的救赎,9.6,美国,剧情,https://movie.douban.com/subject/1292052/,https://img3.doubanio.com/p480747492.jpg
霍伊特团队,9.0,香港,动作,https://movie.douban.com/subject/1307914/,https://img3.doubanio.com/p2329853674.jpg

去除重复？


"""

all_locations = ['大陆','美国','香港','台湾','日本','韩国','英国','法国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']

"""
地区自动获取：
locationList=[]
#用两个next_sibling调出“地区”选项
for child in soup.find(class_='tags').find(class_='category').next_sibling.next_sibling:
    location=child.find(class_='tag').get_text()
    if location!='全部地区':
        locationList.append(location)
"""

myMovies = getAllMovies(['音乐','爱情','文艺'], all_locations)#‘全部地区’和'全部类型'，在url里为空

#把结果myMovies写入csv文件
with codecs.open('movies.csv','w','utf_8_sig') as csv_file:
#with open('movies.csv', 'w', newline='') as csv_file:# 设置newline，否则两行之间会空一行
	spamwriter = csv.writer(csv_file)
	for movie in myMovies:
		spamwriter.writerow(movie)

"""
爬取的电影信息中包含【中文】，如果在导出的时候不指定编码格式，
最后导出的csv使用excel打开会显示乱码，这里建议使用codecs模块解决：

import codecs
...
with codecs.open('movies.csv','w','utf_8_sig') as f:
...
这里先将codecs模块导入，然后使用codecs.open()指定编码格式，这样导出的文件中就不会出现乱码。

"""


"""
任务6: 统计电影数据

统计你【所选取】的【每个电影类别】中，数量排名【前三】的【地区】有哪些，分别占此类别电影总数的【百分比】为多少？

你可能需要自己把这个任务拆分成多个步骤，
统计每个【类别】的电影个数，
统计每个【类别】每个【地区】的电影个数，
排序找到【最大值】，做一定的数学运算等等，相信你一定可以的！

请将你的结果【输出文件】 【output.txt】
"""
#排序后取前三名，输出tuple
def getTop3(movies):
	movie_dict = {}
	for movie in movies:
		if movie[2] not in movie_dict:
			movie_dict[movie[2]] = 1
		else:
			movie_dict[movie[2]] += 1
	movie_dict_sorted = sorted(movie_dict.items(),key = lambda x:x[1], reverse = True)#返回一个list
	return movie_dict_sorted[0][0],movie_dict_sorted[1][0],movie_dict_sorted[2][0]

def getPercentage(movies,i):
	n=0
	for movie in movies:
		if movie[2]==getTop3(movies)[i]:
			n+=1
	#return round((n/len(movies)) *100,2)
	return n/len(movies)
"""
在指定 format 格式时，可以使用下面这种格式，这样就不用手动给百分比乘 100 了：
print("{:.2%} percent.".format(percentage))
"""

#打印
def printTop3(category,movies):
	loc1,loc2,loc3 = getTop3(movies)
	p1 = getPercentage(movies,0)
	p2 = getPercentage(movies,1)
	p3 = getPercentage(movies,2)
	return "The top-3 {} movies are: {}, {} and {}, occupying {:.2%}, {:.2%} and {:.2%}, respectively".format(category,loc1,loc2,loc3,p1,p2,p3)

#【全部地区】的【爱情】【音乐】【文艺】电影
love_movies = getAllMovies(['爱情'],all_locations)#‘全部地区’在url里为空
music_movies = getAllMovies(['音乐'],all_locations)
art_movies = getAllMovies(['文艺'],all_locations)

#输出到文件txt
with open("output.txt", "w") as text_file:
    print(printTop3('love',love_movies) + "\n" + printTop3('music', music_movies) + "\n"+ printTop3('art', art_movies), file=text_file)

"""

请提交submit.zip, 包含以下文件：

DoubanCrawler.py
movies.csv
output.txt

不要提交其他任何文件

注意运行 python 【DoubanCrawler.py】 后，
脚本应该会在同一个文件夹【生成】 movies.csv 和 output.txt 两个文件。
"""
