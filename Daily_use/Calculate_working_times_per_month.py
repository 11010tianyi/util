#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'tianyi'
__date__ = '2023/9/7 10:57 '
__file__ = 'Calculate_working_times_per_month.py'

#Calculate the number and time of working days per month


import datetime
import calendar

def get_business_days(year, month):
    num_days = calendar.monthrange(year, month)[1]
    business_days = 0

    for day in range(1, num_days + 1):
        date = datetime.date(year, month, day)
        if date.weekday() < 5:  # 0-4代表周一至周五
            business_days += 1

    return business_days

def get_business_hours(business_days, hours_per_day):
    return business_days * hours_per_day

# 获取当前年份和月份
current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month

# 假设每个工作日的工作时间为8小时
hours_per_day = 8

# 计算本月的工作日数量和工作小时数
business_days_count = get_business_days(current_year, current_month)
business_hours_count = get_business_hours(business_days_count, hours_per_day)

print("本月工作日数量：", business_days_count)
print("本月工作小时数：", business_hours_count)