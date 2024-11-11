import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from io import StringIO

from selenium.webdriver.common.by import By

# 添加 src 目录到模块搜索路径，以便可以导入 src 目录中的模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from weibo_client import WeiBoClient
from logger import LOG  # 导入日志记录器


class TestWeiBoClient(unittest.TestCase):
    def setUp(self):
        self.client = WeiBoClient()

    @patch('weibo_client.webdriver.Chrome')
    def test_fetch_top_stories_success(self, MockChrome):
        # 创建一个假的 Chrome 实例
        mock_driver = MagicMock()
        MockChrome.return_value = mock_driver
        # 模拟 driver.get 方法
        mock_driver.get.return_value = None

        # 模拟 find_elements 方法
        mock_row = MagicMock()
        mock_row.find_element.return_value = MagicMock(text='热搜 1')  # 模拟找到热搜的标题
        mock_row.find_element.return_value.get_attribute.return_value = 'https://example.com/1'
        mock_driver.find_elements.return_value = [mock_row] * 3  # 假设返回 3 个热搜行

        # 调用方法并验证返回值
        trending_stories = self.client.fetch_trending()
        # 验证 fetch_trending 是否返回了正确的内容
        self.assertEqual(len(trending_stories), 3)
        self.assertEqual(trending_stories[0]['title'], '热搜 1')
        self.assertEqual(trending_stories[0]['link'], 'https://example.com/1')

        # 确保 find_elements 被正确调用
        mock_driver.find_elements.assert_called_once_with(By.CSS_SELECTOR, 'table tbody tr')

        # 确保 get 和 quit 被正确调用
        mock_driver.get.assert_called_once_with(self.client.url)
        mock_driver.quit.assert_called_once()

    @patch('weibo_client.os.makedirs')  # 模拟 os.makedirs，避免创建目录
    @patch('weibo_client.open')  # 模拟 open，以避免实际写入文件
    # @patch('weibo_client.webdriver.Chrome')
    def test_export_trending(self, mock_open, mock_makedirs):
        # 设置时间
        mock_datetime = MagicMock()
        mock_datetime.now.return_value.strftime.return_value = '2024-11-11'  # 假设返回日期为2024-11-11
        datetime = mock_datetime

        # 设置模拟的 WebDriver
        # mock_driver = MagicMock()
        # MockChrome.return_value = mock_driver

        # 模拟 fetch_trending 返回值
        trending_stories = [
            {'title': '热搜 1', 'link': 'https://example.com/1', 'heat': '10000'},
            {'title': '热搜 2', 'link': 'https://example.com/2', 'heat': '9000'}
        ]
        client = WeiBoClient()
        client.fetch_trending = MagicMock(return_value=trending_stories)

        # 调用 export_trending 方法
        file_path = client.export_trending(date='2024-11-11', hour='12')

        # 验证文件路径是否正确生成
        self.assertEqual(file_path, 'weibo\\2024-11-11\\12.md')

        # 验证 open 被正确调用
        mock_open.assert_called_once_with('weibo\\2024-11-11\\12.md', 'w')

        # 验证 os.makedirs 被调用，确保文件夹创建
        mock_makedirs.assert_called_once_with('weibo\\2024-11-11', exist_ok=True)

        # 验证写入文件内容
        file_handle = mock_open.return_value.__enter__.return_value
        file_handle.write.assert_any_call('# Weibo Trending (2024-11-11 12:00)\n\n')
        file_handle.write.assert_any_call('1. [热搜 1 10000](https://example.com/1) \n')


if __name__ == '__main__':
    unittest.main()
