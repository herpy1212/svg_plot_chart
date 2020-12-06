# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:43:29 2020

@author: herpy
"""


from cairosvg import svg2png
import numpy as np

graph_width = 1120

graph_height = 920

y_range = np.arange(30,190,10)
x_range= ["10/"+str(x)  for x in range(10,17)]


caption_font_size = 40
label_font_size = 30

font_family = 'Microsoft JhengHei ,sans-serif '

category_label = ['感覺正常', '心悸' , '胸痛' , '疲勞' , '呼吸急促', '頭重腳輕' , '精神不濟' , '其他']
label_max_char_size = 4
category_value = [19, 74, 80 ,19, 33, 10, 15, 1]
caption_font_h = caption_font_size*2
bar_margin = (graph_height-caption_font_h)*0.2
bar_total_h = (graph_height-caption_font_h)*0.6
bar_h = (bar_total_h/len(category_label))
bar_h2 = bar_h*0.65
bar_Max_w = (graph_width*0.85)-label_font_size*(label_max_char_size+0.5)

svg_code = "<?xml version='1.0' standalone='no'?>"

svg_code += "<svg width='%.2f' height='%.2f' version='1.1' xmlns='http://www.w3.org/2000/svg'>" %(graph_width , graph_height)
svg_code += "<defs> <style type='text/css'><![CDATA["
svg_code += ".bar { height: 21px;}"
svg_code += ".label {font-family:Microsoft JhengHei ,sans-serif ; font-size: %d;}" %(label_font_size)
svg_code += ".lenged { font-family:Microsoft JhengHei ,sans-serif ; fill: #555; font-size:%d;}" %(label_font_size)
svg_code +=  ".figcaption {font-family:Microsoft JhengHei, sans-serif; font-size:%d; font-weight: bold; color: #000; margin-bottom: 20px; }" %(caption_font_size)
svg_code +=  ".feeling1 { fill: #449697;} .feeling2{ fill: #8fc779;} .feeling3{ fill: #e76f73; } .feeling4{fill: #79a3d7;} .feeling5{fill: #37873c;} .feeling6{fill: #d02526;} .feeling7{fill: #1c61ae;} .feeling8{fill: #040000;}"

svg_code += "]]></style></defs>"

x = graph_width*0.05
y = caption_font_size
svg_code +="<text class = 'figcaption' x='%.2f' y='%.2f'>%s</text>" %(x, y, "您的感覺結果統計")

y = caption_font_h + bar_margin
bar_code = ""
for i in range(len(category_label)):
    bar_code += "<g class='bar'>" 
    y = caption_font_h + bar_margin + (bar_h*i)
    x = graph_width*0.05
    bar_code += "<text class = 'lenged' x='%.2f' y='%.2f'>%s</text>" %(x, y, category_label[i])
    x += label_font_size*(label_max_char_size+0.5)
    bar_w = category_value[i]/100*bar_Max_w
    bar_code += "<rect class = 'feeling%d' width='%.2f' height='%.2f' x = '%.2f' y = '%.2f' ></rect>" %(i, bar_w , bar_h2, x , y-label_font_size)
    x += bar_w+label_font_size*0.5
    bar_code += "<text class = 'lenged' x='%.2f' y='%.2f'>%s</text>" %(x, y, str(category_value[i]) + '%')
    bar_code += '</g>'

svg_code += bar_code
svg_code += "</svg>"

svg2png(bytestring=svg_code,write_to='bar_chart.png')

#svg2svg(bytestring=svg_code,write_to='output.svg')

f = open("bar_chart.svg",'w')
f.write(svg_code.replace('\n', '').replace("\'", "'"))
f.close()