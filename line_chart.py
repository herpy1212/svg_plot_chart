# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:43:29 2020

@author: herpy
"""


from cairosvg import svg2png
import numpy as np

graph_width = 1028

graph_height = 306

y_range = np.arange(30,190,10)
x_range= ["10/"+str(x)  for x in range(10,17)]

 
xticks =  (graph_width* 0.85)/(len(x_range)-1)
x_label_ticks = [(graph_width* 0.1)+i*xticks for i in range(len(x_range)) ]

yticks =  (graph_height* 0.85)/(len(y_range)-1)
y_label_ticks = [(graph_height* 0.9)-i*yticks for i in range(len(y_range)) ]

label_font_size = 20

circle_r = 5
circle_width = 4
grid_width = 2
line_width = 3
font_family = 'Microsoft JhengHei ,sans-serif '

svg_code = "<?xml version='1.0' standalone='no'?>"
svg_code += "<svg width='%.2f' height='%.2f' version='1.1' xmlns='http://www.w3.org/2000/svg'>" %(graph_width , graph_height)
svg_code += "<defs> <style type='text/css'><![CDATA["
svg_code += ".labels.x-labels {text-anchor: middle;} .labels.y-labels {text-anchor: end;}"
svg_code += ".grid {stroke: #ccc;stroke-dasharray: 0;stroke-width: %d;} .grid2 {stroke: #ccc; stroke-dasharray: 20, 10;stroke-width: %d;}" %(3,3)
svg_code += ".labels {font-size: %s ; font-family : %s ;text-align:left;} " %(str(label_font_size), font_family)
svg_code += ".data_max {stroke : #e76f73;}.data_min {stroke : #8fc779;}.data_mean{stroke : #79a3d7;}"
svg_code += ".data_line {fill:none;stroke-width:%d;}" %(line_width)
svg_code += ".data_point {fill:white; stroke-width:%d;}" %(circle_width)
svg_code += "]]></style></defs>"



x_label_code = "<g class='grid' id='xGrid'> <line x1='%.2f' x2='%.2f' y1='%.2f' y2='%.2f'></line></g>" %(x_label_ticks[0], x_label_ticks[0], y_label_ticks[0] , y_label_ticks[-1])
y_label_code = "<g class='grid' id='yGrid'> <line x1='%.2f' x2='%.2f' y1='%.2f' y2='%.2f'></line></g>" %(x_label_ticks[0], x_label_ticks[-1], y_label_ticks[0] , y_label_ticks[0])

limit_code = "<g class='grid2' id='Grid_limit'>"
HR_upperlimit_y = y_label_ticks[0] - (100-y_range[0])/10*yticks
limit_code += "<line x1='%.2f' x2='%.2f' y1='%.2f' y2='%.2f'></line>"  %(x_label_ticks[0], x_label_ticks[-1], HR_upperlimit_y , HR_upperlimit_y)
HR_lowerlimit_y = y_label_ticks[0] - (60-y_range[0])/10*yticks
limit_code += "<line x1='%.2f' x2='%.2f' y1='%.2f' y2='%.2f'></line>"  %(x_label_ticks[0], x_label_ticks[-1], HR_lowerlimit_y , HR_lowerlimit_y)
x = graph_width*0.75
y = HR_upperlimit_y + (HR_lowerlimit_y - HR_upperlimit_y)*0.75
limit_code += "</g>"
limit_code += "<text class='labels' fill='#6C6C6C' x='%.2f' y='%.2f'>%s</text>" %(x, y, '屬於正常範圍')

lenged_label = ['MAX','MEAN','MIN']
lenged_class = ['data_max','data_mean','data_min']
legend_width = graph_width*0.1 if graph_width*0.1 > label_font_size*8 else label_font_size*8
legend_height = label_font_size*len(lenged_label)*1.5 + label_font_size*0.5 
lenged_x = x_label_ticks[-1]-legend_width*1.05
lenged_y = y_label_ticks[-1]+legend_height*0.05


lenged_code = "<g class='labels'>"
lenged_code +="<rect class='grid' x = '%.2f' y = '%.2f' width='%.2f' height='%.2f' fill='none'/>" %(lenged_x, lenged_y, legend_width, legend_height)

lenged_line_len = legend_width*0.4


for i in range(len(lenged_label)):
    x = legend_width*0.05 + lenged_x
    y = lenged_y + (i*1.5+1)*label_font_size
    lenged_code += "<line class = 'data_line %s' x1='%.2f' x2='%.2f' y1='%.2f' y2='%.2f'> </line>" %(lenged_class[i], x, x + lenged_line_len, y, y)
    lenged_code += "<circle class= 'data_point %s' cx='%.2f' cy='%.2f' r = '%d'></circle>" %(lenged_class[i], x + lenged_line_len*0.5, y, circle_r)
    x = x + lenged_line_len + label_font_size
    y = y + 0.5*label_font_size
    lenged_code += "<text x='%.2f' y='%.2f'>%s</text>"  %(x, y, lenged_label[i])
    
lenged_code +="</g>"


svg_code += x_label_code
svg_code += y_label_code
svg_code += limit_code
svg_code += lenged_code


y = y_label_ticks[0] + label_font_size * 1.5
x_label_code = """<g class='labels x-labels'>"""
for i in range(len(x_range)):
    x_label_code += "<text x='%.2f' y='%.2f'>%s</text>" %(x_label_ticks[i],y,str(x_range[i]))
x_label_code += "</g>"
svg_code += x_label_code


x = x_label_ticks[0] - label_font_size * 1
y_label_code = """<g class='labels y-labels'>"""
for i in range(len(y_range)):
    y_label_code += "<text x='%.2f' y='%.2f'>%s</text>" %(x,y_label_ticks[i]+label_font_size*0.25,str(y_range[i]))

y_label_code += "</g>"
svg_code += y_label_code


data_array_max = [80,100,78,105,70,60,65]

polyline_code =  "<polyline  class = 'data_max data_line' points= '"
circle_code = "<g class='data_max'>"
for i in range(len(data_array_max)):
    x = x_label_ticks[i]
    y = y_label_ticks[0] - (data_array_max[i]-y_range[0])/10*yticks
    polyline_code += " %.2f,%.2f " %(x, y)
    circle_code += "<circle class= 'data_point' cx='%.2f' cy='%.2f' r = '%d' data-value='%.2f'></circle>" %(x, y, circle_r, data_array_max[i])
    
circle_code += "</g>"
polyline_code += "'/>"

svg_code += polyline_code
svg_code += circle_code


data_array_mean = [60,80,75,95,65,55,60]

polyline_code =  "<polyline  class = 'data_mean data_line' points= '"
circle_code = "<g class='data_mean'>"
for i in range(len(data_array_mean)):
    x = x_label_ticks[i]
    y = y_label_ticks[0] - (data_array_mean[i]-y_range[0])/10*yticks
    polyline_code += " %.2f,%.2f " %(x, y)
    circle_code += "<circle class= 'data_point' cx='%.2f' cy='%.2f' r = '%d' data-value='%.2f'></circle>" %(x, y, circle_r, data_array_mean[i])

circle_code += "</g>"
polyline_code += "'/>"

svg_code += polyline_code
svg_code += circle_code


data_array_min = [55,75,50,60,55,40,50]

polyline_code =  "<polyline  class = 'data_min data_line' points= '"
circle_code = "<g class='data_min'>"
for i in range(len(data_array_min)):
    x = x_label_ticks[i]
    y = y_label_ticks[0] - (data_array_min[i]-y_range[0])/10*yticks
    polyline_code += " %.2f,%.2f " %(x, y)
    circle_code += "<circle class= 'data_point' cx='%.2f' cy='%.2f' r = '%d' data-value='%.2f'></circle>" %(x, y, circle_r, data_array_min[i])
    
circle_code += "</g>"
polyline_code += "'/>"

svg_code += polyline_code
svg_code += circle_code


svg_code += "</svg>"


svg2png(bytestring=svg_code,write_to='line_chart.png')

#svg2svg(bytestring=svg_code,write_to='output.svg')

f = open("line_chart.svg",'w')
f.write(svg_code.replace('\n', '').replace("\'", "'"))
f.close()