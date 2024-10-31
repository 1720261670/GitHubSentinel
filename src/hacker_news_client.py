
import requests  # 导入requests库用于HTTP请求
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta  # 导入日期处理模块
import os  # 导入os模块用于文件和目录操作
from logger import LOG  # 导入日志模块

class HackerNewsClient:
    def fetch_hackernews_hot_posts(self):
        url = 'https://news.ycombinator.com/'
        response = requests.get(url)

        print(f"Response Status Code: {response.status_code}")  # 打印状态码

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            hot_posts = []

            # 更新选择器，使用 '.titleline' 选择器
            for item in soup.select('.titleline a'):
                title = item.get_text()
                link = item['href']
                hot_posts.append({'title': title, 'link': link})

            return hot_posts
        else:
            print("Failed to retrieve data")
            return []

    def export_daily_progress(self):
        # .isoformat()
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取今天的日期
        LOG.debug(f"[准备导出项目进度]：{today}")
        hot_posts = self.fetch_hackernews_hot_posts() # 获取今天的数据

        repo_dir = os.path.join('hackernews', today.replace(":", "_"))  # 构建存储路径
        os.makedirs(repo_dir, exist_ok=True)  # 确保目录存在

        file_path = os.path.join(repo_dir, f'{today.replace(":", "_")}.md')  # 构建文件路径
        with open(file_path, 'w') as file:
            file.write(f"# Daily Hotspot for ({today})\n\n")
            if hot_posts:
                for index, post in enumerate(hot_posts, start=1):
                    file.write(f"{index}. {post['title']} - {post['link']}\n")
            else:
                file.write(f"No hot posts found.")
        LOG.info(f"[hackernews项目每日热点文件生成： {file_path}")  # 记录日志
        return file_path,today
if __name__ == '__main__':
    hot_posts = HackerNewsClient().export_daily_progress()
    # if hot_posts:
    #     for index, post in enumerate(hot_posts, start=1):
    #         print(f"{index}. {post['title']} - {post['link']}")
    # else:
    #     print("No hot posts found.")
