import json
from typing import Dict
from urllib.parse import urljoin

import requests
from loguru import logger


class NotifyBot(object):
    def __init__(self, content, title="什么值得买签到", **kwargs: Dict) -> None:
        self.content = content
        self.title = title
        self.kwargs = kwargs

        self.bark()
        #self.push_plus()
        #self.server_chain()
        #self.wecom()
        #self.tg_bot()

    def bark(self):
        if not self.kwargs.get("BARK_URL", None):
            logger.warning("⚠️ BARK_URL not set, skip Bark notification")
            return
        url = self.kwargs.get("BARK_URL")
        title = self.title
        content = self.content
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        json_data = {
            'body': self.content,
            'title': self.title,
            # 'badge': 1,
            'category': 'myNotificationCategory',
            'sound': 'silence',
            'icon': 'https://gh.xiaozl.cf/https://raw.githubusercontent.com/metowolf/vCards/master/data/%E7%94%B5%E5%95%86%E8%B4%AD%E7%89%A9/%E4%BB%80%E4%B9%88%E5%80%BC%E5%BE%97%E4%B9%B0.png',
            'group': 'smzdm',
            # 'url': 'https://mritd.com',
        }
        try:
            resp = requests.post(url, headers=headers, json=json_data,timeout=(10,5))
            if resp.ok:
                logger.info("✅ bark notified")
            else:
                logger.warning("Fail to notify bark")
        except Exception as e:
            logger.error(e)

    def push_plus(self, template="html"):
        if not self.kwargs.get("PUSH_PLUS_TOKEN", None):
            logger.warning("⚠️ PUSH_PLUS_TOKEN not set, skip PushPlus nofitication")
            return
        PUSH_PLUS_TOKEN = self.kwargs.get("PUSH_PLUS_TOKEN")

        url = "https://www.pushplus.plus/send"
        body = {
            "token": PUSH_PLUS_TOKEN,
            "title": self.title,
            "content": self.content,
            "template": template,
        }
        data = json.dumps(body).encode(encoding="utf-8")
        headers = {"Content-Type": "application/json"}
        try:
            resp = requests.post(url, data=data, headers=headers)
            if resp.ok:
                logger.info("✅ Push Plus notified")
            else:
                logger.warning("Fail to notify Push Plus")
        except Exception as e:
            logger.error(e)

    def server_chain(self):
        if not self.kwargs.get("SC_KEY", None):
            logger.warning("⚠️ SC_KEY not set, skip ServerChain notification")
            return
        SC_KEY = self.kwargs.get("SC_KEY")
        url = f"http://sc.ftqq.com/{SC_KEY}.send"
        data = {"text": self.title, "desp": self.content}
        try:
            resp = requests.post(url, data=data)
            if resp.ok:
                logger.info("✅ Server Chain notified")
            else:
                logger.warning("Fail to notify Server Chain")
        except Exception as e:
            logger.error(e)

    def wecom(self):
        if not self.kwargs.get("WECOM_BOT_WEBHOOK", None):
            logger.warning("⚠️ WECOM_BOT_WEBHOOK not set, skip WeCom notification")
            return
        WECOM_BOT_WEBHOOK = self.kwargs.get("WECOM_BOT_WEBHOOK")
        message = {
            "msgtype": "text",
            "text": {"content": f"{self.title}\n{self.content}"},
        }
        try:
            resp = requests.post(WECOM_BOT_WEBHOOK, data=json.dumps(message))
            if resp.ok:
                logger.info("✅ WeCom notified")
            else:
                logger.warning("Fail to notify WeCom")
        except Exception as e:
            logger.error(e)

    def tg_bot(self):
        if not self.kwargs.get("TG_BOT_TOKEN", None) or not self.kwargs.get(
            "TG_USER_ID", None
        ):
            logger.warning("⚠️ Skip TelegramBot notification")
            return
        TG_BOT_TOKEN = self.kwargs.get("TG_BOT_TOKEN")
        TG_USER_ID = self.kwargs.get("TG_USER_ID")
        if self.kwargs.get("TG_BOT_API"):
            url = urljoin(
                self.kwargs.get("TG_BOT_API"), f"/bot{TG_BOT_TOKEN}/sendMessage"
            )
        else:
            url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {
            "chat_id": str(TG_USER_ID),
            "text": f"{self.title}\n{self.content}",
            "disable_web_page_preview": "true",
        }
        try:
            resp = requests.post(url=url, headers=headers, params=params)
            if resp.ok:
                logger.info("✅ Telegram Bot notified")
            else:
                logger.warning("Fail to notify TelegramBot")
        except Exception as e:
            logger.error(e)
