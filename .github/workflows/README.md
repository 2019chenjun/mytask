# GitHub Actions 工作流配置说明

## 设置步骤

### 1. 配置 GitHub Secrets

在 GitHub 仓库中设置以下 Secrets：

#### 必需配置：
- **GR_COOKIE**: GLaDOS 账号的 Cookie
  - 获取方式：登录 GLaDOS 网站后，在浏览器开发者工具中复制 Cookie
  - 格式：`koa:sess=xxx; koa:sess.sig=xxx`
  - 多个账号：用 `&` 或换行符分隔

#### 可选配置：
- **GR_PROXY**: 代理服务器地址（如果 IP 被封禁）
  - 单个代理：`http://proxy.example.com:8080`
  - 多个代理（代理池）：`http://proxy1.com:8080|http://proxy2.com:8080`
  - 带认证：`http://user:pass@proxy.example.com:8080`
  - SOCKS5：`socks5://proxy.example.com:1080`

### 2. 设置 Secrets 的方法

1. 进入 GitHub 仓库
2. 点击 **Settings**（设置）
3. 左侧菜单选择 **Secrets and variables** → **Actions**
4. 点击 **New repository secret**
5. 输入名称和值，点击 **Add secret**

### 3. 定时任务说明

- **执行时间**：每天 UTC 16:40（对应北京时间 00:40）
- **时区说明**：GitHub Actions 使用 UTC 时间
  - 北京时间 = UTC + 8
  - 如果要修改时间，编辑 `.github/workflows/checkin.yml` 中的 `cron` 表达式

### 4. Cron 表达式格式

```
分钟 小时 日 月 星期
40   16   *  *  *    # 每天 16:40 UTC
```

### 5. 手动触发

- 在 GitHub 仓库的 **Actions** 标签页
- 选择 **GLaDOS 自动签到** 工作流
- 点击 **Run workflow** 按钮

### 6. 查看执行结果

- 在 **Actions** 标签页查看工作流执行历史
- 点击每次运行查看详细日志
- 如果失败，可以下载日志文件

## 注意事项

1. **Cookie 安全**：Cookie 包含登录凭证，请妥善保管，不要泄露
2. **代理配置**：如果 IP 被封禁，建议配置代理
3. **执行时间**：确保定时任务时间设置正确
4. **依赖更新**：如果添加新依赖，更新 `requirements.txt`

