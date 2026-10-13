# GLaDOS 自动签到脚本

自动签到 GLaDOS 账号的 Python 脚本，支持本地运行和 GitHub Actions 自动执行。

## 功能特性

- ✅ 自动签到 GLaDOS 账号
- ✅ 支持多账号签到
- ✅ 支持代理配置（HTTP/HTTPS/SOCKS5）
- ✅ IP 检测和封禁检测
- ✅ 反检测机制（随机 User-Agent、请求延迟等）
- ✅ 自动重试机制
- ✅ 飞书/企业微信/Telegram 等通知支持
- ✅ GitHub Actions 自动执行

## 使用方法

### 方式一：本地运行

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **配置 Cookie**
   
   编辑 `config.py` 文件，设置你的 Cookie：
```python
Cookies = [
    '你的Cookie1',
    '你的Cookie2'
]
```

3. **运行脚本**
```bash
python3 checkin.py
```

### 方式二：GitHub Actions 自动执行（推荐）

1. **Fork 或克隆此仓库**

2. **配置 GitHub Secrets**
   
   在仓库设置中添加以下 Secrets：
   - `GR_COOKIE`: GLaDOS Cookie（必填）
   - `GR_PROXY`: 代理地址（可选）

   详细配置说明见 [.github/workflows/README.md](.github/workflows/README.md)

3. **启用 GitHub Actions**
   
   - 进入仓库的 **Actions** 标签页
   - 点击 **I understand my workflows, enable them**

4. **手动触发测试**
   
   - 在 **Actions** 页面选择 **GLaDOS 自动签到**
   - 点击 **Run workflow** 测试

5. **定时执行**
   
   - 默认每天 UTC 16:40（北京时间 00:40）自动执行
   - 可在 `.github/workflows/checkin.yml` 中修改时间

## 配置说明

### Cookie 获取方法

1. 登录 [GLaDOS](https://glados.rocks)
2. 打开浏览器开发者工具（F12）
3. 进入 **Network** 标签
4. 刷新签到页或点一次签到，找到 `/api/user/status` 或 `/api/user/checkin` 请求
5. 在请求头中找到 `Cookie`，复制完整内容

**必含字段（2026 新验签）：**

```text
koa:sess=...; koa:sess.sig=...; gld:sess=gld_...; gld:sess.sig=...
```

- 缺少 `gld:sess` / `gld:sess.sig` 会返回 `没有权限`
- `__stripe_mid` 可忽略，与鉴权无关
- 多账号在 `config.py` 用列表，或在环境变量 `GR_COOKIE` 用 `&` / 换行分隔
- 脚本会先从 `/api/user/sessions` 读取登录设备的 User-Agent；如读取失败，可设置
  `GLADOS_USER_AGENT` 为浏览器登录时使用的完整 User-Agent。

### 代理配置（可选）

如果 IP 被封禁，可以配置代理：

#### 方式1：环境变量
```bash
export GR_PROXY="http://proxy.example.com:8080"
```

#### 方式2：配置文件
编辑 `config.py`：
```python
# 单个代理
Proxies = "http://proxy.example.com:8080"

# 代理池（自动切换）
Proxies = [
    "http://proxy1.com:8080",
    "http://proxy2.com:8080"
]
```

#### 方式3：GitHub Secrets
在 GitHub Secrets 中设置 `GR_PROXY`

### 通知配置

编辑 `sendNotify.py` 配置通知方式：
- 飞书机器人
- 企业微信
- Telegram
- 钉钉
- Server酱
- 等等

## 文件说明

- `checkin.py` - 主签到脚本
- `config.py` - 配置文件（Cookie、代理等）
- `sendNotify.py` - 通知服务
- `requirements.txt` - Python 依赖
- `.github/workflows/checkin.yml` - GitHub Actions 工作流

## 注意事项

1. **Cookie 安全**：请妥善保管 Cookie，不要泄露
2. **IP 封禁**：如果遇到 104 错误，建议配置代理
3. **定时任务**：GitHub Actions 使用 UTC 时间，注意时区转换
4. **依赖更新**：添加新功能时记得更新 `requirements.txt`

## 常见问题

### Q: 返回「没有权限」怎么办？
A: Cookie 缺少新会话字段。请重新从浏览器复制完整 Cookie，必须包含 `gld:sess` 和 `gld:sess.sig`（不能只复制 `koa:sess`）。

### Q: 出现 104 错误怎么办？
A: 这是连接被重置，可能是 IP 被封禁。建议：
- 配置代理服务器
- 增加重试次数
- 检查网络连接

### Q: 如何修改定时执行时间？
A: 编辑 `.github/workflows/checkin.yml` 中的 `cron` 表达式：
```yaml
schedule:
  - cron: '40 16 * * *'  # 分钟 小时 日 月 星期（北京时间 00:40）
```

### Q: 如何添加多个账号？
A: 在 Cookie 配置中用 `&` 或换行符分隔多个 Cookie

### Q: 如何查看执行日志？
A: 在 GitHub Actions 页面查看每次运行的详细日志

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

