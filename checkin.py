#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: checkin.py(GLaDOS签到)
Author: Hennessey
Date: 2023/3/22 18:59
cron: 40 0 * * *
new Env('GLaDOS签到');
Update: 2023/5/7 优化信息输出效果,新增本地运行
"""


import requests
import json
import os
import sys
import time
import random
import gzip

# 获取代理配置
def get_proxies():
    """获取代理配置，支持环境变量和配置文件"""
    # 优先使用环境变量
    if os.environ.get("GR_PROXY"):
        proxy = os.environ["GR_PROXY"]
        if proxy and proxy.lower() != "none":
            # 支持多个代理，用|分隔
            if '|' in proxy:
                proxies_list = [p.strip() for p in proxy.split('|')]
                return proxies_list
            return proxy

    # 使用配置文件
    try:
        from config import Proxies
        if Proxies:
            if isinstance(Proxies, list):
                return Proxies
            return Proxies
    except:
        pass

    return None

# 检测当前IP地址
def get_current_ip(proxies=None):
    """获取当前出口IP地址"""
    ip_check_urls = [
        "https://api.ipify.org?format=json",
        "https://ifconfig.me/ip",
        "https://api.ip.sb/ip",
    ]

    for url in ip_check_urls:
        try:
            response = requests.get(url, timeout=10, proxies=proxies)
            if response.status_code == 200:
                try:
                    data = response.json()
                    ip = data.get('ip', response.text.strip())
                except:
                    ip = response.text.strip()
                return ip
        except:
            continue
    return None

# 检测IP是否被封禁
def check_ip_blocked(proxies=None):
    """检测IP是否被封禁，尝试访问目标网站"""
    test_url = "https://glados.cloud"
    try:
        response = requests.get(
            test_url,
            timeout=10,
            proxies=proxies,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        # 如果返回403/429等，可能被封禁
        if response.status_code in [403, 429]:
            return True, f"HTTP状态码: {response.status_code}"
        return False, None
    except requests.exceptions.ConnectionError as e:
        # 连接错误可能是被封禁
        return True, f"连接错误: {str(e)}"
    except Exception as e:
        return False, None

# 获取GlaDOS账号Cookie
def get_cookies():
    if os.environ.get("GR_COOKIE"):
        print("已获取并使用Env环境 Cookie")
        if '&' in os.environ["GR_COOKIE"]:
            cookies = os.environ["GR_COOKIE"].split('&')
        elif '\n' in os.environ["GR_COOKIE"]:
            cookies = os.environ["GR_COOKIE"].split('\n')
        else:
            cookies = [os.environ["GR_COOKIE"]]
    else:
        from config import Cookies
        cookies = Cookies
        if len(cookies) == 0:
            print("未获取到正确的GlaDOS账号Cookie")
            return
    print(f"共获取到{len(cookies)}个GlaDOS账号Cookie\n")
    print(f"脚本执行时间(北京时区): {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}\n")
    return cookies


# 加载通知服务
def load_send():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/sendNotify.py"):
        try:
            from sendNotify import send
            return send
        except Exception as e:
            print(f"加载通知服务失败：{e}")
            return None
    else:
        print("加载通知服务失败")
        return None


# 生成随机User-Agent，模拟真实浏览器
def get_random_user_agent():
    """返回随机的真实浏览器User-Agent"""
    user_agents = [
        # Chrome on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        # Chrome on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        # Edge on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        # Firefox on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    ]
    return random.choice(user_agents)

# GlaDOS签到
def checkin(cookie, max_retries=3, proxies=None):
    checkin_url= "https://glados.cloud/api/user/checkin"
    state_url= "https://glados.cloud/api/user/status"
    console_url = "https://glados.cloud/console/checkin"
    referer = 'https://glados.cloud/console/checkin'
    origin = "https://glados.cloud"

    # 随机选择User-Agent
    useragent = get_random_user_agent()

    payload={
        'token': 'glados.cloud'
    }

    # 模拟真实浏览器的完整请求头
    headers = {
        'cookie': cookie,
        'referer': referer,
        'origin': origin,
        'user-agent': useragent,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'accept-encoding': 'gzip, deflate',
        'content-type': 'application/json;charset=UTF-8',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
    }

    # 使用Session保持连接，减少连接重置问题
    # 配置连接池和重试适配器
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    session = requests.Session()
    session.headers.update(headers)

    # 设置代理
    if proxies:
        if isinstance(proxies, list):
            # 代理池：随机选择一个
            proxy = random.choice(proxies)
        else:
            proxy = proxies

        # 配置代理
        if proxy.startswith('socks5://') or proxy.startswith('socks4://'):
            # SOCKS代理需要安装requests[socks]
            try:
                import socks
                session.proxies = {
                    'http': proxy,
                    'https': proxy
                }
            except ImportError:
                print(f"警告: SOCKS代理需要安装requests[socks]，当前使用HTTP代理格式")
                session.proxies = {
                    'http': proxy.replace('socks5://', 'http://').replace('socks4://', 'http://'),
                    'https': proxy.replace('socks5://', 'http://').replace('socks4://', 'http://')
                }
        else:
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
        print(f"使用代理: {proxy}")

    # 配置重试策略，兼容新旧版本的urllib3
    try:
        # 新版本urllib3使用allowed_methods
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
    except TypeError:
        # 旧版本urllib3使用method_whitelist
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["GET", "POST"]
        )

    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=1,  # 限制连接池大小
        pool_maxsize=1
    )
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # 重试机制
    for attempt in range(max_retries):
        try:
            # 模拟真实浏览器：先访问控制台页面（可选，但更真实）
            if attempt == 0:
                # 第一次尝试时，先访问控制台页面，模拟用户打开页面
                try:
                    console_headers = {
                        'cookie': cookie,
                        'user-agent': useragent,
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                        'accept-encoding': 'gzip, deflate',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'none',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                    }
                    session.get(console_url, headers=console_headers, timeout=(10, 15))
                    # 模拟用户停留时间
                    time.sleep(random.uniform(1, 3))
                except:
                    pass  # 如果访问控制台失败，继续执行签到

            # 添加超时设置，并在请求前稍作延迟，避免请求过快
            if attempt > 0:
                time.sleep(random.uniform(2, 5))  # 随机延迟2-5秒

            # 添加超时设置
            checkin_response = session.post(
                checkin_url,
                data=json.dumps(payload),
                timeout=(10, 30),  # (连接超时, 读取超时)
                allow_redirects=True
            )

            # 检查HTTP状态码
            if checkin_response.status_code != 200:
                if attempt < max_retries - 1:
                    print(f"签到请求失败，HTTP状态码：{checkin_response.status_code}，正在重试... ({attempt + 1}/{max_retries})")
                    time.sleep(2)  # 等待2秒后重试
                    continue
                else:
                    print(f"签到请求失败，HTTP状态码：{checkin_response.status_code}")
                    return None, None, None

            # 获取状态信息，两个请求之间随机延迟（模拟真实用户行为）
            time.sleep(random.uniform(0.5, 1.5))

            # 更新状态请求的头部（GET请求的头部略有不同）
            state_headers = {
                'cookie': cookie,
                'referer': referer,
                'user-agent': useragent,
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'accept-encoding': 'gzip, deflate',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
            }
            state_response = session.get(
                state_url,
                headers=state_headers,
                timeout=(10, 30),
                allow_redirects=True
            )

            if state_response.status_code != 200:
                if attempt < max_retries - 1:
                    print(f"获取状态失败，HTTP状态码：{state_response.status_code}，正在重试... ({attempt + 1}/{max_retries})")
                    time.sleep(2)
                    continue
                else:
                    print(f"获取状态失败，HTTP状态码：{state_response.status_code}")
                    return None, None, None

            # 解析响应
            try:
                # requests库已自动解压gzip，直接使用text
                checkin_text = checkin_response.text
                state_text = state_response.text

                # 如果原始内容是gzip格式（未被requests解压），手动解压
                if checkin_response.content[:2] == b'\x1f\x8b':
                    checkin_text = gzip.decompress(checkin_response.content).decode('utf-8')
                if state_response.content[:2] == b'\x1f\x8b':
                    state_text = gzip.decompress(state_response.content).decode('utf-8')

                checkin_data = json.loads(checkin_text)
                state_data = json.loads(state_text)

                mess = checkin_data.get('message', '未知')
                mail = state_data.get('data', {}).get('email', 'unknown')
                left_days = float(state_data['data']["leftDays"])

                return mess, left_days, mail

            except (KeyError, ValueError, json.JSONDecodeError) as e:
                print(f"解析响应数据失败：{e}")
                if attempt < max_retries - 1:
                    print(f"正在重试... ({attempt + 1}/{max_retries})")
                    time.sleep(2)
                    continue
                else:
                    return None, None, None

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < max_retries - 1:
                print(f"网络连接失败：{e}，正在重试... ({attempt + 1}/{max_retries})")
                time.sleep(3)  # 连接错误等待更长时间
                continue
            else:
                print(f"签到失败，请检查网络：{e}")
                return None, None, None
        except Exception as e:
            print(f"签到失败，未知错误：{type(e).__name__}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                return None, None, None
        finally:
            session.close()

    return None, None, None


# 执行签到任务
def run_checkin():
    contents = []
    cookies = get_cookies()
    if not cookies:
        return ""

    # 获取代理配置
    proxies = get_proxies()

    # 检测IP状态
    if proxies:
        if isinstance(proxies, list):
            current_proxy = random.choice(proxies)
        else:
            current_proxy = proxies
        print(f"检测代理IP状态...")
        current_ip = get_current_ip({'http': current_proxy, 'https': current_proxy})
        if current_ip:
            print(f"当前代理IP: {current_ip}")
        else:
            print("警告: 无法获取代理IP，代理可能不可用")
    else:
        print("检测出口IP状态...")
        current_ip = get_current_ip()
        if current_ip:
            print(f"当前出口IP: {current_ip}")
        else:
            print("警告: 无法获取出口IP")

        # 检测IP是否被封禁
        is_blocked, reason = check_ip_blocked()
        if is_blocked:
            print(f"⚠️  警告: IP可能被封禁 - {reason}")
            print("建议: 配置代理或更换服务器IP")
            # 可以选择继续执行或退出
            # return "IP被封禁，无法执行签到"

    for cookie in cookies:
        # 多个账号之间随机延迟，避免请求过于规律
        ret, remain, email = checkin(cookie, proxies=proxies)
        if not ret:
            continue

        content = f"账号：{email}\n签到结果：{ret}\n剩余天数：{remain}\n"
        print(content)
        contents.append(content)

        # 多个账号之间随机延迟，模拟真实用户切换账号的时间
        if cookie != cookies[-1]:  # 不是最后一个账号
            delay = random.uniform(3, 8)
            time.sleep(delay)

    contents_str = "".join(contents)
    return contents_str


if __name__ == '__main__':
    title = "GlaDOS签到通知"
    contents = run_checkin()
    send_notify = load_send()
    if send_notify:
        if contents =='':
            contents=f'签到失败，请检查账户信息以及网络环境'
            print(contents)
        send_notify(title, contents)
