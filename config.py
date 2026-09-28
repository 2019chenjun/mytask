Cookies = [
    # 账号1：需同时包含 koa:* 与 gld:*（2026 新验签）
    "koa:sess=eyJ1c2VySWQiOjkwNTYzLCJfZXhwaXJlIjoxODExNjU1MzI5NDMyLCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=; koa:sess.sig=YCqnH-64Ae2r-xRk-drTaUxwLC4; gld:sess=gld_24606a8374ebb4d0e6cf763e56dc2eaccb88b180d3ea2741; gld:sess.sig=DD1SYIUc8GsmPcq8X-_m1P_lWbc",
    # 账号2：请重新从浏览器抓取完整 Cookie（必须含 gld:sess / gld:sess.sig），否则会返回「没有权限」
    "koa:sess=eyJ1c2VySWQiOjY5MzI5OCwiX2V4cGlyZSI6MTgxMzA1NzcwMTgxMCwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=ZPrU6nk8FfpIXEYJjTABv5nMH-0; gld:sess=gld_cc41870ede9ebfc1443f3f1911ec8769980edbb9e1394e30; gld:sess.sig=-AkXK06xAP7Sa2s8LNEZa_rd31A",
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
