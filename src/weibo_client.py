from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os  # 导入os模块用于文件和目录操作
from logger import LOG  # 导入日志模块
from datetime import datetime  # 导入datetime模块用于获取日期和时间


class WeiBoClient:
    def __init__(self):
        self.url = 'https://s.weibo.com/top/summary'

    def fetch_trending(self):
        LOG.debug("准备获取微博的热搜。")
        # 设置Chrome选项（不打开浏览器窗口）
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # 启动WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        # 访问微博热搜榜
        driver.get(self.url)
        # 等待页面加载完成
        time.sleep(3)
        # 找到热搜榜的表格
        LOG.debug("解析微博的HTML内容。")
        rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        trending_stories = []
        # 输出热搜榜信息
        for row in rows:
            # 获取热搜标题和链接
            title = row.find_element(By.CSS_SELECTOR, 'td.td-02').text
            link = row.find_element(By.CSS_SELECTOR, 'td.td-02 a').get_attribute('href')
            heat = row.find_element(By.CSS_SELECTOR, 'td.td-03').text
            # print(f'热搜: {title}，热度: {heat}，链接：{link}')
            trending_stories.append({'title': title, 'link': link, 'heat': heat})
        LOG.info(f"成功解析 {len(trending_stories)} 条微博热搜。")
        # 关闭浏览器
        driver.quit()
        return trending_stories

    def export_trending(self, date=None, hour=None):
        LOG.debug("准备导出微博的热搜。")
        trending_stories = self.fetch_trending()  # 获取热搜数据

        if not trending_stories:
            LOG.warning("未找到任何微博的热搜。")
            return None

        # 如果未提供 date 和 hour 参数，使用当前日期和时间
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        if hour is None:
            hour = datetime.now().strftime('%H')

        # 构建存储路径
        dir_path = os.path.join('weibo', date)
        os.makedirs(dir_path, exist_ok=True)  # 确保目录存在

        file_path = os.path.join(dir_path, f'{hour}.md')  # 定义文件路径
        with open(file_path, 'w') as file:
            file.write(f"# Weibo Trending ({date} {hour}:00)\n\n")
            for idx, story in enumerate(trending_stories, start=1):
                file.write(f"{idx}. [{story['title']} {story['heat']}]({story['link']}) \n")

        LOG.info(f"微博热搜文件生成：{file_path}")
        return file_path


if __name__ == "__main__":
    client = WeiBoClient()
    client.export_trending()  # 默认情况下使用当前日期和时间
