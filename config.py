Cookies = [
    # 账号1：需同时包含 koa:* 与 gld:*（2026 新验签）
"koa:sess=eyJ1c2VySWQiOjkwNTYzLCJfZXhwaXJlIjoxODExNjU1MzI5NDMyLCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=; koa:sess.sig=YCqnH-64Ae2r-xRk-drTaUxwLC4; gld:sess=gld_1e368a43dbc444a3afd6ee2480cef5e008bc426002f0e181; gld:sess.sig=dTKkqIcoix0whUpOPWnyNpCnrvo"
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
