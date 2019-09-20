# -*- coding: utf-8 -*-

import time

def handle_html(cur_mode, state):
    html = """<html>
<meta http-equiv="refresh" content="2" />
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="apple-mobile-web-app-capable" content="yes">

<head>
<title>Home heating control</title>
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-dark-grey.css">
</head>
<body bgcolor="#303030">"""

    html += "<h1 style='text-align:center;color:white;'>%s</h1>\n" % cur_mode
    html += "<p style='text-align:center;color:white;'>Аптайм: %s мин (%s сек)</p>\n" % (int(time.time()/60), time.time())
    html += "<p style='text-align:center;color:white;'>%s</p>\n" % state
    html += """
<form method='POST' action='/low' align="center">
<input type="submit" value="Минимум" style="width:80%; font-size:25px;">
</form>
<form method='POST' action='/mid' align="center">
<input type="submit" value="Среднее" style="width:80%;font-size:25px;">
</form>
<form method='POST' action='/high' align="center">
<input type="submit" value="Максимум" style="width:80%;font-size:25px;">
</form>
<form method='POST' action='/off' align="center">
<input type="submit" value="Выключить" style="width:80%;font-size:25px;">
</form>
</body>
</html>"""
    return html

