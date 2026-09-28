Cookies = [
    "koa:sess=eyJ1c2VySWQiOjkwNTYzLCJfZXhwaXJlIjoxODExNjU1MzI5NDMyLCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=; koa:sess.sig=YCqnH-64Ae2r-xRk-drTaUxwLC4",
    "koa:sess=eyJ1c2VySWQiOjY5MzI5OCwiX2V4cGlyZSI6MTgxMzA1NzcwMTgxMCwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=ZPrU6nk8FfpIXEYJjTABv5nMH-0"
]

# 代理配置（可选）
# 支持格式：
# 1. 单个代理: "http://proxy.example.com:8080"
# 2. 多个代理（代理池）: ["http://proxy1.com:8080", "http://proxy2.com:8080"]
# 3. 带认证的代理: "http://user:pass@proxy.example.com:8080"
# 4. SOCKS5代理: "socks5://proxy.example.com:1080"
Proxies = None  # 设置为None表示不使用代理
# Proxies = "http://proxy.example.com:8080"  # 单个代理
# Proxies = ["http://proxy1.com:8080", "http://proxy2.com:8080"]  # 代理池
