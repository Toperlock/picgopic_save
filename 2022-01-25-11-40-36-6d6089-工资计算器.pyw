import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import re
import json
import urllib.request


def get_money():
    url = "http://hq.sinajs.cn/list=USDCNY"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    f=urllib.request.urlopen(req).read()
    html = f
    USDCNY = float(str(html).split(",")[-3])
    return USDCNY
    
class calMoney(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setWindowTitle('工资计算器')
        self.resize(300, 100)

        # 定义QLable时，在快捷键字母前加“&”符号；
        # alt+P
        MoneyLabel = QLabel("&提款额:")
        self.inpMoney = QDoubleSpinBox()
        self.inpMoney.setPrefix("$ ") # 设置前缀
        self.inpMoney.setRange(0,1000000)
        self.inpMoney.setValue(10000)
        MoneyLabel.setBuddy(self.inpMoney)

        PerLabel = QLabel("&提款额百分比:")
        self.inpPer = QDoubleSpinBox()
        self.inpPer.setSuffix(" %") # 设置后缀
        self.inpPer.setDecimals(3)
        self.inpPer.setValue(2)
        PerLabel.setBuddy(self.inpPer)

        UsePerDIYLabel = QLabel("&使用自定义百分比(默认不使用):")
        self.inpUsePerDIY = QComboBox()
        self.inpUsePerDIY.addItems(['Yes','No']) #是否使用
        self.inpUsePerDIY.setCurrentIndex(1) #默认不使用
        UsePerDIYLabel.setBuddy(self.inpUsePerDIY)

        Money1Label = QLabel("&底薪:")
        self.inpMoney1 = QDoubleSpinBox()
        self.inpMoney1.setPrefix("￥ ") # 设置前缀
        self.inpMoney1.setRange(0,1000000)
        self.inpMoney1.setValue(4500)
        Money1Label.setBuddy(self.inpMoney1)

        OverTimeLabel = QLabel("&加班天数:")
        self.inpOverTime = QDoubleSpinBox()
        self.inpOverTime.setSuffix(" 天 ") # 设置前缀
        self.inpOverTime.setRange(0,31)
        self.inpOverTime.setDecimals(0)
        self.inpOverTime.setValue(0)
        OverTimeLabel.setBuddy(self.inpOverTime)

        RateLabel = QLabel("&实时汇率:")
        self.oupRate = QLabel(" ")
        RateLabel.setBuddy(self.oupRate)
        
        
        '''BonusLabel = QLabel("&绩效奖金按实时汇率算:")
        self.oupBonus = QLabel("￥")
        BonusLabel.setBuddy(self.oupBonus)'''

        Bonus1Label = QLabel("&绩效奖金按汇率6.3算:")
        self.oupBonus1 = QLabel("￥")
        Bonus1Label.setBuddy(self.oupBonus1)

        '''WageLabel = QLabel("&工资按实时汇率算:")
        self.oupWage = QLabel("￥4500")
        WageLabel.setBuddy(self.oupWage)'''

        Wage1Label = QLabel("&工资按汇率6.3算:")
        self.oupWage1 = QLabel("￥4500")
        Wage1Label.setBuddy(self.oupWage1)

        OverTime_PayLabel = QLabel("&加班费:")
        self.oupOverTime_Pay = QLabel("￥0")
        OverTime_PayLabel.setBuddy(self.oupOverTime_Pay)

        Totall_PayLabel = QLabel("&总工资按汇率6.3算:")
        self.oupTotall_Pay = QLabel("￥")
        Totall_PayLabel.setBuddy(self.oupTotall_Pay)

        Text1Label = QLabel("1万美金以内2%")
        Text2Label = QLabel("1-3万美金部分2.2%")
        Text3Label = QLabel("3万美金以上部分2.5%")

        # 网格布局
        layout = QGridLayout()
        layout.addWidget(MoneyLabel, 0, 0)
        layout.addWidget(self.inpMoney, 0, 1)
        layout.addWidget(PerLabel, 1, 0)
        layout.addWidget(self.inpPer, 1, 1)
        layout.addWidget(UsePerDIYLabel, 2, 0)
        layout.addWidget(self.inpUsePerDIY, 2, 1) 
        layout.addWidget(Money1Label, 3, 0)
        layout.addWidget(self.inpMoney1, 3, 1)
        layout.addWidget(OverTimeLabel, 4, 0)
        layout.addWidget(self.inpOverTime, 4, 1)
        layout.addWidget(RateLabel, 5, 0)
        layout.addWidget(self.oupRate, 5, 1)
        '''layout.addWidget(BonusLabel, 6, 0)
        layout.addWidget(self.oupBonus, 6, 1)'''
        layout.addWidget(Bonus1Label, 7, 0)
        layout.addWidget(self.oupBonus1, 7, 1)
        '''layout.addWidget(WageLabel, 8, 0)
        layout.addWidget(self.oupWage, 8, 1)'''
        layout.addWidget(Wage1Label, 9, 0)
        layout.addWidget(self.oupWage1, 9, 1)
        layout.addWidget(OverTime_PayLabel, 10, 0)
        layout.addWidget(self.oupOverTime_Pay, 10, 1)
        layout.addWidget(Totall_PayLabel, 11, 0)
        layout.addWidget(self.oupTotall_Pay, 11, 1)
        layout.addWidget(Text1Label, 12, 0)
        layout.addWidget(Text2Label, 13, 0)
        layout.addWidget(Text3Label, 14, 0)

        # 信号与槽相连
        self.inpMoney.valueChanged.connect(self.updateAmount)
        self.inpPer.valueChanged.connect(self.updateAmount)
        self.inpUsePerDIY.currentIndexChanged.connect(self.updateAmount)
        self.inpMoney1.valueChanged.connect(self.updateAmount)
        self.inpOverTime.valueChanged.connect(self.updateAmount)

        self.setLayout(layout)

    def updateAmount(self):
        
        money = float(self.inpMoney.value()) #提款额
        money1 = float(self.inpMoney1.value()) #底薪
        per = float(self.inpPer.value()) #百分比
        #bonus = money * (0.01 * per) * USDCNY
        useper = str(self.inpUsePerDIY.currentText())
        if useper == 'No':
            if money > 30000:
                over = float((money - 30000) * (0.01 * 2.5) * 6.3)
                over1 = float(10000 * (0.01 * 2.2) * 6.3)
                bonus1 = float(10000 * (0.01 * 2) * 6.3 + over +over1)
            elif money > 10000 and money <20000:
                over = float((money - 10000) * (0.01 * 2.2) * 6.3)
                bonus1 = float(10000 * (0.01 * 2) * 6.3 + over)
            else:
                bonus1 = float(money * (0.01 * 2) * 6.3)
        else:
            bonus1 = float(money * (0.01 * per) * 6.3)

        overtime_pay = self.inpOverTime.value() * 50 #加班费
        #wage = money1 + bonus
        wage1 = money1 + bonus1
        totall_pay = wage1 + overtime_pay
        self.oupRate.setText("{0:.3f}".format(USDCNY))
        #self.oupBonus.setText('￥' + "{0:.2f}".format(bonus))
        self.oupBonus1.setText('￥' + "{0:.2f}".format(bonus1))
        #self.oupWage.setText('￥' + "{0:.2f}".format(wage))
        self.oupWage1.setText('￥' + "{0:.2f}".format(wage1))
        self.oupOverTime_Pay.setText('￥' + "{0:.2f}".format(overtime_pay))
        self.oupTotall_Pay.setText('￥' + "{0:.2f}".format(totall_pay))
        pass

app = QApplication(sys.argv)
USDCNY = get_money()
form = calMoney()
form.show()
app.exec_()
