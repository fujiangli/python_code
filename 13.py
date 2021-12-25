import requests
from lxml import etree
import json


class UsstRequest(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def request(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
            'Connection': 'keep-alive',
        }
        session = requests.Session()
        # 得到登录页面的url
        url_1 = 'http://jwgl.usst.edu.cn/sso/jziotlogin'
        response_1 = session.get(url=url_1, headers=headers)
        url_2 = response_1.url
        response_2 = session.get(url=url_2, headers=headers)
        tree = etree.HTML(response_2.text)
        lt, dt, exe, _e, rm = tree.xpath('//*[@id="casLoginForm"]/input/@value')
        # 表单数据
        data = {
            'username': self.username,
            'password': self.password,
            'lt': lt,
            'dllt': dt,
            'execution': exe,
            '_eventId': _e,
            'rmShown': rm
        }
        # 发请求以获得返回的cookie
        url_3 = url_2
        response_3 = session.post(url=url_3, headers=headers, data=data)
        # 对课表发请求的表单数据
        data = {
            'xnm': '2021',
            'xqm': '12',
            'kzlx': 'ck'
        }
        # 获取个人课表的数据
        url_4 = 'http://jwgl.usst.edu.cn/jwglxt/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N253508&su={}'.format(self.username)
        response_4 = session.post(url=url_4, headers=headers, data=data)
        if response_4.url == url_4:
            dic = json.loads(response_4.text)['kbList']
            class_dict = {}
            # 提取有效信息
            for i in dic:
                list1 = [[i['kcmc'], i['xm'], i['cdmc'], i['jc']]]
                class_dict[i['xqjmc']] = class_dict.get(i['xqjmc'], [[i['kcmc'], i['xm'], i['cdmc'], i['jc']]]) + list1
                #       课程名称   老师       周几        上课地点     节次
                print(i['kcmc'], i['xm'], i['xqjmc'], i['cdmc'], i['jc'])
            print(class_dict)
        else:
            print('用户名或密码错误!')


if __name__ == '__main__':
    username = input('输入学号:')
    password = input('输入密码:')
    class_table = UsstRequest(username, password)
    class_table.request()
