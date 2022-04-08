# Author: Klaus
# Date: 2022/4/8 16:37

import requests
from bilibiliapi import *

class BiliBiliCheckIn(object):
    # 待测试，需要大会员账号测试领取福利
    def __init__(self, bilibili_cookie_list):
        self.bilibili_cookie_list = bilibili_cookie_list

    @staticmethod
    def get_nav(session):
        url = "https://api.bilibili.com/x/web-interface/nav"
        ret = session.get(url=url).json()
        # print(ret) #取消本段输出
        uname = ret.get("data", {}).get("uname")
        uid = ret.get("data", {}).get("mid")
        is_login = ret.get("data", {}).get("isLogin")
        coin = ret.get("data", {}).get("money")
        vip_type = ret.get("data", {}).get("vipType")
        current_exp = ret.get("data", {}).get("level_info", {}).get("current_exp")
        return uname, uid, is_login, coin, vip_type, current_exp

    @staticmethod
    def manga_sign(session, platform="android") -> dict:
        """
        模拟B站漫画客户端签到
        """
        try:
            url = "https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn"
            post_data = {"platform": platform}
            ret = session.post(url=url, data=post_data).json()
            if ret["code"] == 0:
                msg = "签到成功"
            elif ret["msg"] == "clockin clockin is duplicate":
                msg = "今天已经签到过了"
            else:
                msg = f'签到失败，信息为({ret["message"]})'
        except Exception as e:
            msg = f"签到异常,原因为: {str(e)}"
        return msg


    @staticmethod
    def manga_trade(session, platform="android") -> dict:
        """
        模拟B站漫画客户端兑换
        """
        quan_id = 0
        try:
            # url = "https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/ListProduct"
            # post_data = {"platform": platform}
            # ret = session.post(url=url, data=post_data).json()
            # print(ret['msg'])
            # if ret["code"] == 0:
            #     for obj in ret['data']:
            #         if obj['type'] ==7:
            #             quan_id = obj['id']
            #             real_cost = obj['real_cost']
            #             print('id获取成功——'+ quan_id)

            url_trade = 'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/Exchange'
            post_data = {"product_id": 195, 'product_num': 1, 'point': 100}
            ret = session.post(url=url_trade, data=post_data).json()
            if ret['code'] == 0:
                msg = '兑换成功'
            elif ret['code'] == 1:
                msg = '积分不足'
            elif ret['code'] == 2:
                msg = '库存不足'
            elif ret['code'] == 3:
                msg = '超过用户最大可兑换数量'
            elif ret['code'] == 4:
                msg = '现在抢票的人太多啦，再点一下有机会优先上车喔 ε=ε=(ノ≧∇≦)ノ'
            else:
                msg = ret['msg']

            # else:
            #     msg = f'兑换失败，信息为({ret["message"]})'
        except Exception as e:
            msg = f"兑换异常,原因为: {str(e)}"
        return msg

    def main(self):
        msg_list = []
        bilibili_cookie = self.bilibili_cookie_list
        bili_jct = bilibili_cookie.get("bili_jct")

        session = requests.session()
        requests.utils.add_dict_to_cookiejar(session.cookies, bilibili_cookie)
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/63.0.3239.108",
                "Referer": "https://www.bilibili.com/",
                "Connection": "keep-alive",
            }
        )
        success_count = 0
        uname, uid, is_login, coin, vip_type, current_exp = self.get_nav(session=session)
        # print(uname, uid, is_login, coin, vip_type, current_exp)
        if is_login:
            manhua_msg = self.manga_sign(session=session)
            print(manhua_msg)
            trade_msg = self.manga_trade(session=session)
            print(trade_msg)


if __name__ == "__main__":

    BILI_USER = ""
    BILI_PASS = ""
    BILI_COOKIE = "buvid3=E184A75D-9D1D-4EFA-AFF8-CC153733F406143097infoc; blackside_state=1; rpdid=|(k|mmJlYYuJ0J'uY|RYRJRYk; LIVE_BUVID=AUTO1616051701845447; _uuid=BAB1F15F-FF91-0A7B-B53D-13F1978B0A1A57330infoc; video_page_version=v_old_home; SESSDATA=c497b25e%2C1653472506%2C4d7a6%2Ab1; bili_jct=11ed4d936e0bed091c4602e564d8ed4f; DedeUserID=179081341; DedeUserID__ckMd5=81a7aabdf4d01e0b; sid=7c72p1q6; fingerprint_s=3d5d5ed656c589224f81a5002de4c79d; i-wanna-go-back=-1; b_ut=5; buvid_fp=3c47bcb4307e30b9ac0459c23247d5cf; buvid4=D8737132-918F-49EB-B363-4C99B63D6F2827007-022012116-6b6D/3Z22/jI20/P280BEHUjR7G2BjpOzl3irk6wqPkbkglEPMWiwQ%3D%3D; CURRENT_BLACKGAP=0; nostalgia_conf=-1; CURRENT_QUALITY=0; fingerprint=422f3d32559316a377bbe3fa9d3a5717; fingerprint3=df266f0b28928ddaee9702e0a1e8af1d; bp_video_offset_179081341=646331164398714900; PVID=1; CURRENT_FNVAL=4048; innersign=0; b_lsid=5122827E_18008580E78"
    # 未填写参数取消运行
    if BILI_USER == "" or BILI_PASS == "":
        if BILI_COOKIE == "":
            print("未填写哔哩哔哩账号密码或COOKIE取消运行")
            exit(0)

    if BILI_COOKIE == "":
        b = Bilibili()
        login = b.login(username=BILI_USER, password=BILI_PASS)
        if login == False:
            exit(0)
        _bilibili_cookie_list = b.get_cookies()
    else:
        _bilibili_cookie_list = {cookie.split('=')[0]:cookie.split('=')[-1] for cookie in BILI_COOKIE.split(';')}

    BiliBiliCheckIn(bilibili_cookie_list=_bilibili_cookie_list).main()
