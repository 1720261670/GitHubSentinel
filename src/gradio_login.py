import gradio as gr
from config import Config  # 导入配置管理模块
from github_client import GitHubClient  # 导入用于GitHub API操作的客户端
from report_generator import ReportGenerator  # 导入报告生成器模块
from llm import LLM  # 导入可能用于处理语言模型的LLM类
from subscription_manager import SubscriptionManager  # 导入订阅管理器
import json
import os

# 创建各个组件的实例
config = Config()
github_client = GitHubClient(config.github_token)
llm = LLM()
report_generator = ReportGenerator(llm)
subscription_manager = SubscriptionManager(config.subscriptions_file)

# 简单的用户数据库
user_db = {
    "admin": "admin",
    "user": "user",
}

def export_progress_by_date_range(repo, days):
    # 定义一个函数，用于导出和生成指定时间范围内项目的进展报告
    raw_file_path = github_client.export_progress_by_date_range(repo, days)  # 导出原始数据文件路径
    report, report_file_path = report_generator.generate_report_by_date_range(raw_file_path, days)  # 生成并获取报告内容及文件路径

    return report, report_file_path  # 返回报告内容和报告文件路径

# 模拟用户登录验证
def login(username, password):
    if username in user_db and user_db[username] == password:
        session_token = f"token_for_{username}"
        return f"Login successful for {username}", session_token
    else:
        return "Login failed", None


# 退出功能
def logout():
    return (gr.update(visible=True), gr.update(visible=False), "Logged out successfully.", None, "")


# 登录并切换页面
def login_and_switch(username, password):
    status, token = login(username, password)
    if token:
        # 登录成功，返回隐藏登录页面，显示受保护页面，并更新受保护页面内容
        if username == "admin":
            role = "admin"
        else:
            role = "user"
        return gr.update(visible=False), gr.update(visible=True), status, token, role
    else:
        # 登录失败，继续显示登录页面
        return gr.update(), gr.update(visible=False), status, None, None

# JSON 文件路径
DATA_FILE = "subscriptions.json"

# 将一维数组转换为二维数组
def convert_to_2d(data):
    return [[item] for item in data]  # 每个元素放在一个子列表中

# 保存数据到 JSON 文件
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# 添加新数据
def add_data(new_entry, current_data):
    if new_entry and new_entry not in current_data:  # 检查是否已存在
        current_data.append(new_entry)  # 添加新数据
        save_data(current_data)  # 保存到文件
    return gr.update(choices=current_data),gr.update(choices=current_data)  # 返回更新后的数据

# 删除选定的数据
def delete_data(selected_rows, current_data):
    for row in selected_rows:
        current_data.remove(row)
    save_data(current_data)
    return gr.update(choices=current_data),gr.update(choices=current_data)

# 控制按钮的可见性
def toggle_buttons(role):
    if role == "admin":
        return gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)  # 显示新增和删除按钮
    else:
        return gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False)  # 隐藏新增和删除按钮
# 创建 Gradio 界面
with gr.Blocks() as app:
    session_token = gr.State(None)  # 存储 session token

    # 登录页面
    with gr.Column(visible=True) as login_page:
        gr.Markdown("## 用户登录")
        username_input = gr.Textbox(label="用户名")
        password_input = gr.Textbox(label="密码", type="password")
        login_button = gr.Button("登录")
        login_status = gr.Textbox(label="登录状态", interactive=False)
    # 受保护的页面
    with gr.Column(visible=False) as protected_page:
        gr.Markdown("## GitHubSentinel")
        user_role = gr.State(None)  # 存储用户角色
        # 创建一个行以排列输入和输出
        with gr.Row():
            # 左侧输入
            with gr.Column():
                subscribe = gr.Dropdown(
                subscription_manager.list_subscriptions(), label="订阅列表", info="已订阅GitHub项目"
        )# 下拉菜单选择订阅的GitHub项目
                report = gr.Slider(value=2, minimum=1, maximum=7, step=1, label="报告周期",info="生成项目过去一段时间进展，单位：天")
                # 滑动条选择报告的时间范围
                submit_button = gr.Button("生成报告")
                # 添加退出按钮
                logout_button = gr.Button("退出")
                # 显示当前数据
                data_display = gr.Radio(label="订阅列表(选中后可删除)", choices=subscription_manager.list_subscriptions(), interactive=True)

                # 输入新增数据的框
                new_data_input = gr.Textbox(label="新增订阅", placeholder="订阅信息")
                add_button = gr.Button("新增订阅")

                # 删除按钮
                delete_button = gr.Button("删除订阅")

                # 添加新数据
                add_button.click(
                    fn=lambda new_entry: add_data(new_entry, subscription_manager.list_subscriptions()),
                    inputs=new_data_input,
                    outputs=[data_display,subscribe]
                )

                # 删除选定数据
                delete_button.click(
                    fn=lambda selected_entries: delete_data(selected_entries,
                                                            subscription_manager.list_subscriptions()),
                    inputs=data_display,
                    outputs=[data_display,subscribe]
                )

            # 右侧输出
            with gr.Column():
                markdown_output = gr.Markdown()
                file_output = gr.File(label="下载报告")

        # 当点击提交按钮时，显示输入结果
        submit_button.click(
            fn=export_progress_by_date_range,
            inputs=[subscribe, report],
            outputs=[markdown_output, file_output]
        )
        logout_button.click(
            fn=logout,
            inputs=[],
            outputs=[login_page, protected_page, login_status, session_token, user_role]
        )


    # 登录按钮点击事件，触发页面切换
    login_button.click(
        fn=login_and_switch,
        inputs=[username_input, password_input],
        outputs=[login_page, protected_page, login_status, session_token, user_role]
    )
    # 切换按钮可见性
    user_role.change(
        fn=toggle_buttons,
        inputs=user_role,
        outputs=[add_button, delete_button, data_display, new_data_input]
    )


if __name__ == "__main__":
    app.launch(share=True, server_name="0.0.0.0")