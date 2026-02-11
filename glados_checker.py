#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
from typing import Tuple, Optional
import logging

class GladosChecker:
    def __init__(self):
        self.base_url = "https://glados.cloud"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'origin': 'https://glados.cloud',
            'referer': 'https://glados.cloud/console/checkin',
            'content-type': 'application/json;charset=UTF-8'
        }
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger('GladosChecker')

    def check_cookie_validity(self, cookie: str) -> bool:
        """验证Cookie是否有效"""
        try:
            headers = {**self.headers, 'cookie': cookie}
            response = requests.get(f"{self.base_url}/api/user/status", headers=headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Cookie验证失败: {str(e)}")
            return False

    def get_account_status(self, cookie: str) -> Tuple[bool, Optional[float], Optional[str]]:
        """获取账户状态"""
        try:
            headers = {**self.headers, 'cookie': cookie}
            response = requests.get(f"{self.base_url}/api/user/status", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    return True, float(data['data']['leftDays']), data['data'].get('email', 'unknown')
            return False, None, None
        except Exception as e:
            self.logger.error(f"获取账户状态失败: {str(e)}")
            return False, None, None

    def do_checkin(self, cookie: str) -> Tuple[bool, str]:
        """执行签到"""
        try:
            headers = {**self.headers, 'cookie': cookie}
            payload = {'token': 'glados.one'}
            response = requests.post(
                f"{self.base_url}/api/user/checkin",
                headers=headers,
                data=json.dumps(payload),
                timeout=10
            )
            result = response.json()
            return True, result.get('message', '未知结果')
        except Exception as e:
            self.logger.error(f"签到失败: {str(e)}")
            return False, f"签到异常: {str(e)}"

    def process_account(self, cookie: str) -> str:
        """处理单个账户的签到流程"""
        if not self.check_cookie_validity(cookie):
            return "Cookie无效或已过期"

        success, days_left, email = self.get_account_status(cookie)
        if not success:
            return "获取账户状态失败"

        checkin_success, message = self.do_checkin(cookie)
        
        result = (
            f"账号：{email or '未知'}\n"
            f"签到结果：{'成功' if checkin_success else '失败'} - {message}\n"
            f"剩余天数：{days_left if days_left is not None else '未知'}\n"
            f"检查时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        
        self.logger.info(f"处理结果:\n{result}")
        return result

def main():
    """主函数，用于测试"""
    from config import Cookies
    checker = GladosChecker()
    results = []
    
    for cookie in Cookies:
        result = checker.process_account(cookie)
        results.append(result)
        
    final_result = "\n".join(results)
    print(final_result)
    
    # 如果需要发送通知
    try:
        from sendNotify import send
        send("GLaDOS签到结果", final_result)
    except ImportError:
        print("通知模块未找到，仅输出到控制台")

if __name__ == "__main__":
    main()
