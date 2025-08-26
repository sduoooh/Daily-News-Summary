# Daily News Summary

这是一个自动收集和总结新闻的项目，使用GitHub Actions定时运行。

## 功能

- 从多个新闻网站收集新闻
- 使用Google Gemini AI进行新闻摘要
- 通过邮件发送摘要结果(默认使用`QQ`邮箱)

## Todo

### 系统优化

- [ ] 优化结构，`AI Summary`、新闻标题和内容获取、信息上传等部分进一步模块化，便于拓展和更新
- [ ] 提取逻辑中的可变部分作为配置项

### 逻辑更新

- [ ] 支持进一步的新闻完整文章获取`(可选)`
- [ ] 内容持久化、向量化便于查询
- [ ] 支持在`AI Summary`前，根据当前收集的新闻，从向量化的往期内容中提供相关背景以供建立事件发展链
- [ ] 独立化往期内容的管理和获取，并建立便于查询的支持主题化事件发展链聚合的Web UI

### 内容扩展

- [ ] 增加更多新闻源

# 部署方式

## 1. 直接使用Github Actions

### 设置GitHub Secrets

在部署到GitHub Actions之前，需要在你的GitHub仓库中设置以下Secrets：

1. 进入你的GitHub仓库
2. 点击 "Settings" 标签
3. 在左侧菜单中选择 "Secrets and variables" > "Actions"
4. 点击 "New repository secret" 添加以下secrets：

#### 必需的Secrets

- `GEMINI_API_KEY`: 你的Google Gemini API密钥
- `EMAIL_ADDRESS`: 发送邮件的邮箱地址
- `EMAIL_PASSWORD`: 邮箱的授权码（不是登录密码）
- `RECIPIENT_EMAIL`: 接收邮件的邮箱地址

#### 可选的Secrets

- `ZAOBAO_SHADOW`: Github Action IP可访问的联合早报realtime页面URL，置空则不获取该数据

#### QQ邮箱设置说明

如果使用QQ邮箱发送邮件，需要：

1. 登录QQ邮箱
2. 进入设置 > 账户
3. 开启SMTP服务
4. 获取授权码（16位字符串）
5. 将授权码作为 `EMAIL_PASSWORD` 的值

### 定时执行

GitHub Actions工作流配置为每天4点、12点和20点自动运行三次。你也可以在Actions页面手动触发执行。结合该策略，项目中默认使用`9h`作为新闻收集间隔。

#### 自定义执行策略

如需更改定时策略，并需要调整收集间隔，请在`main.py`中对`get_page`函数的调用传入可选的`time_limit`参数以控制收集间隔。
如同时启用了`zaobao`的收集策略，修改收集间隔后，可选地在`main.py`中修改对已排序的新闻列表`res`的二次过滤阈值。

## 2. 本地运行

如果要在本地运行，需要：

1. 安装依赖：`pip install -r requirements.txt`
2. 设置环境变量或直接在 `config.py` 中填入配置
3. 运行：`python main.py`

### 自定义执行策略

同 [`直接使用Github Actions` 部分对应章节](####自定义执行策略)。
