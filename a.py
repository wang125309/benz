#!/usr/bin/env python
# coding=utf-8
import requests
import random
if __name__ == '__main__':
    for i in range(0,10000):
        j = random.randint(1,30)
        requests.get("http://www.360youtu.com/blow_test/add_height/?openid="+str(j))
