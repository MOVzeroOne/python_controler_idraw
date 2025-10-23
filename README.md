<h1> iDraw H A3 pen plotter python api (linux) </h1>

<h2>Examples </h2>
<h3> Drawing a square with incremental increase in speed for each side </h3> </br>

```
pen = AutoPen()

pen.set_pen_height(5) # pen down
pen.move_xy_variable_speed(x=0,y=10,speed=500) 
pen.move_xy_variable_speed(x=10,y=10,speed=1000) 
pen.move_xy_variable_speed(x=10,y=0,speed=1500) 
pen.move_xy_variable_speed(x=0,y=0,speed=2000) 
pen.set_pen_height(0) # pen up 
```

<h3> Drawing a circle </h3> </br>


<h3>Drawing a bunch of circles </h3>


<h3>Draw SVG </h3>

```
pen = AutoPen()

plot_svg(pen=pen,path="./input.svg",temp_gcode_file_path=./output.gcode)
```
![IMG-20251022-WA0009_resized](https://github.com/user-attachments/assets/8cfdf1b6-87d7-4dc0-bd43-108ac98ee50a)

<h3>Draw multilayer drawing (merge multiple seperate svg's, with time between pen swapping)</h3>

```
pen = AutoPen() </br>

multilayer_svg(pen,["multilayer_image/green_layer_resized.svg","multilayer_image/red_layer_resized.svg","multilayer_image/blue_layer_resized.svg"]) </br>
```
(add first layer) </br>
![IMG_20251023_135543149](https://github.com/user-attachments/assets/ee499ced-fc97-4c61-9c78-3822518c2c71)

(add second layer) </br>
![IMG_20251023_113036194](https://github.com/user-attachments/assets/378c1b89-0bed-4418-a09c-be7d871d9f2f)

(add third layer) </br>
![IMG_20251023_113533036](https://github.com/user-attachments/assets/fe8be36a-e157-44e4-a3b8-d91a1d5009be)
