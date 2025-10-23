<h1> iDraw H A3 pen plotter python api (linux) </h1>

<h2> Installation</h2>
only packages used are: </br> 
- tqdm (loading bar) </br>
- pyserial (for serial communication with penplotter) </br> 
- vpype[all] and vpype-gcode (to convert svg to gcodes) </br>
</br>

To make installation easier I made a requirments.txt with frozen version numbers (python version I used is 3.13.9, but I'm quite sure other version will also work), </br>
to install the requirements you can just do </br>

```
pip install -r requirements.txt
```



<h2> Things to know </h2>

When plotting an svg, you should put the pen in the bottom left. </br> </br>
When directly controling the autopen with move_xy and arcs know that the position the pen starts in will be seen as the 0,0 point, and by default all movements 
are absolute coordinates with respect to this point. </br> </br>
Using arcs is a bit odd, you basically have to define a center of the arc relative to the position of the pen, </br>
and then give the position you want to end the arc in absolute coordinates. If the ending coordinates don't end up on the circle who's center you have defined (with I,J) </br>
the instruction will not be valid.


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


https://github.com/user-attachments/assets/396987d8-6b0b-4993-b329-576341d77da2



<h3> Drawing a circle </h3> 

```
pen = AutoPen()

pen.set_pen_height(5) # pen down
pen.arc_clock_wise(0,0,2,2)
pen.set_pen_height(0) # pen up 

```

https://github.com/user-attachments/assets/f5f96751-55c2-492e-af7b-0c8af98b03b2



<h3> Drawing a chain </h3> 

```
pen = AutoPen()

pen.set_pen_height(5) # pen down
pen.arc_clock_wise(4,8,2,4) #new pos is (4,8)
pen.arc_clock_wise(8,16,2,4) #new pos is (8,16)
pen.arc_clock_wise(12,24,2,4) #new pos is (12,24)
pen.arc_clock_wise(8,16,-2,-4) #new pos is (8,16)
pen.arc_clock_wise(4,8,-2,-4) #new pos is (4,8)
pen.arc_clock_wise(0,0,-2,-4) #new pos is (0,0)
pen.set_pen_height(0) # pen up 

pen.move_xy_variable_speed(2,0) #move to (2,0)
pen.set_pen_height(5) # pen down
pen.arc_counter_clock_wise(6,8,2,4) #new pos is (6,8)
pen.arc_counter_clock_wise(10,16,2,4) #new pos is (10,16)
pen.arc_counter_clock_wise(14,24,2,4) #new pos is (14,24)
pen.arc_counter_clock_wise(10,16,-2,-4) #new pos is (8,16)
pen.arc_counter_clock_wise(6,8,-2,-4) #new pos is (4,8)
pen.arc_counter_clock_wise(2,0,-2,-4) #new pos is (0,0)
pen.set_pen_height(0) # pen up
pen.move_xy_variable_speed(0,0) #move to start
```


https://github.com/user-attachments/assets/8944ef7c-10d1-4a28-b685-544d12f16e68



<h3>Draw SVG </h3>

```
pen = AutoPen()

plot_svg(pen=pen,image_path="./input.svg",temp_gcode_file_path="./output.gcode")
```
![IMG-20251022-WA0009_resized](https://github.com/user-attachments/assets/8cfdf1b6-87d7-4dc0-bd43-108ac98ee50a)

<h3>Draw multilayer drawing (merge multiple seperate svg's, with time between pen swapping)</h3>

```
pen = AutoPen()

multilayer_svg(pen,["multilayer_image/green_layer_resized.svg","multilayer_image/red_layer_resized.svg","multilayer_image/blue_layer_resized.svg"]) 
```
(add first layer) </br>
![IMG_20251023_135543149](https://github.com/user-attachments/assets/ee499ced-fc97-4c61-9c78-3822518c2c71)

(add second layer) </br>
![IMG_20251023_113036194](https://github.com/user-attachments/assets/378c1b89-0bed-4418-a09c-be7d871d9f2f)

(add third layer) </br>
![IMG_20251023_113533036](https://github.com/user-attachments/assets/fe8be36a-e157-44e4-a3b8-d91a1d5009be)
