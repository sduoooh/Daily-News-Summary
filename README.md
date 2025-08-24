# Daily News Summary

这是一个自动收集和总结新闻的项目，使用GitHub Actions定时运行。

## 功能

- 从多个新闻网站收集新闻
- 使用Google Gemini AI进行新闻摘要
- 通过邮件发送摘要结果(默认使用`QQ`邮箱)

## 设置GitHub Secrets

在部署到GitHub Actions之前，需要在你的GitHub仓库中设置以下Secrets：

1. 进入你的GitHub仓库
2. 点击 "Settings" 标签
3. 在左侧菜单中选择 "Secrets and variables" > "Actions"
4. 点击 "New repository secret" 添加以下secrets：

### 必需的Secrets

- `GEMINI_API_KEY`: 你的Google Gemini API密钥
- `EMAIL_ADDRESS`: 发送邮件的邮箱地址
- `EMAIL_PASSWORD`: 邮箱的授权码（不是登录密码）
- `RECIPIENT_EMAIL`: 接收邮件的邮箱地址

### 可选的Secrets

- `ZAOBAO_SHADOW`: Github Action IP可访问的联合早报realtime页面URL，置空则不获取该数据

### QQ邮箱设置说明

如果使用QQ邮箱发送邮件，需要：

1. 登录QQ邮箱
2. 进入设置 > 账户
3. 开启SMTP服务
4. 获取授权码（16位字符串）
5. 将授权码作为 `EMAIL_PASSWORD` 的值

## 定时执行

GitHub Actions工作流配置为每天4点、12点和20点自动运行三次。你也可以在Actions页面手动触发执行。

## 本地运行

如果要在本地运行，需要：

1. 安装依赖：`pip install -r requirements.txt`
2. 设置环境变量或直接在 `config.py` 中填入配置
3. 运行：`python main.py`
