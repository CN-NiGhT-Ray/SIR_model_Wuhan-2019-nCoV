from raybasiclib import Connect
import matplotlib.pyplot as plt
import json

class Sir:

    def __init__(self, ls_i, ls_r, NUM):
        if len(ls_i) != len(ls_r):
            exit('init error！')
        self.ls_s = [NUM - i - r for (i, r) in zip(ls_i, ls_r)]
        self.ls_i = ls_i
        self.ls_r = ls_r
        b_num = 0
        g_num = 0
        temp_s = 0
        temp_i = 0
        temp_r = 0
        t = 0
        flag = True
        for (s, i, r) in zip(self.ls_s, self.ls_i, self.ls_r):
            t += 1
            if t == 50:
                break
            if t > 13:
                if flag:
                    flag = False
                else:
                    b_num += (i - temp_i) / temp_s / temp_i
                    g_num += (r - temp_r) / temp_i
                temp_s = s
                temp_i = i
                temp_r = r
        self.b = b_num / (t - 10)
        self.g = g_num / (t - 10)
        print('b: {}\ng: {}'.format(self.b, self.g))

    def forecast(self, T):
        t = len(self.ls_r)
        if t >= T:
            print('预测失败：预测天数({})<=数据记录天数({})'.format(T, t))
            exit('程序退出')
        s = self.ls_s[-1]
        i = self.ls_i[-1]
        r = self.ls_r[-1]
        fls_s = []
        fls_i = []
        fls_r = []
        while t <= T:
            dsi = self.b * s * i
            dr = self.g * i
            s -= dsi
            i += (dsi - dr)
            r += dr
            fls_s.append(s)
            fls_i.append(i)
            fls_r.append(r)
            t += 1
        self.ls_s += fls_s
        self.ls_i += fls_i
        self.ls_r += fls_r


'''connection = Connect(proxies={'http': '127.0.0.1', 'https': '127.0.0.1'})
json = json.load(connection.get('https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json'))'''
with open('data/Wuhan-2019-nCoV.json', encoding='utf-8') as file:
    json = json.load(file)
ls_confirmed = []
ls_cured = []
for i in json:
    if i['cityCode'] == '420100':
        ls_confirmed.append(i['confirmed'])
        ls_cured.append(i['cured'])
test = Sir(ls_confirmed, ls_cured, 9083500)
test.forecast(720)
t = range(len(test.ls_r))
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.figure(num='zzy', figsize=(12, 6))
plt.title('SIR模型')
plt.xlabel('时间(天)')
plt.ylabel('人数')
plt.plot(t, test.ls_s, label='易感染者', color='sandybrown')
plt.plot(t, test.ls_i, label='感染者', color='lightcoral')
plt.plot(t, test.ls_r, label='移除者', color='greenyellow')
for h, i, j, k in zip(t, test.ls_s, test.ls_i, test.ls_r):
    plt.scatter(h, i, 3, 'b')
    plt.scatter(h, j, 3, 'b')
    plt.scatter(h, k, 3, 'b')
plt.legend(loc='center left')
plt.show()
input()
