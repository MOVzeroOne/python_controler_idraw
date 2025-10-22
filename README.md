<h1> iDraw H A3 pen plotter python api (linux) </h1>

<h2>Examples </h2>
<h3> Drawing a square with incremental increase in speed for each side </h3> </br>
pen = AutoPen() </br>

pen.set_pen_height(5) # pen down</br>
pen.move_xy_variable_speed(x=0,y=10,speed=500) </br>
pen.move_xy_variable_speed(x=10,y=10,speed=1000) </br>
pen.move_xy_variable_speed(x=10,y=0,speed=1500) </br>
pen.move_xy_variable_speed(x=0,y=0,speed=2000) </br>
pen.set_pen_height(0) # pen up </br>

<h3> Drawing a circle </h3> </br>


<h3>Drawing a bunch of circles </h3>


<h3>Draw SVG </h3>
pen = AutoPen() </br>

plot_svg(pen=pen,path="./input.svg",temp_gcode_file_path=./output.gcode)  </br>
![IMG_20251022_162823830](https://github.com/user-attachments/assets/da515e2e-edfd-44ec-938c-7219ce425578)

<h3>Draw multilayer drawing (merge multiple seperate svg's, with time between pen swapping)</h3>
pen = AutoPen() </br>

multilayer_svg(pen,["multilayer_image/lion_plotted_1_set1_pen1_100 Black.svg","multilayer_image/lion_plotted_1_set1_pen2_YR09 Chinese Orange.svg","multilayer_image/lion_plotted_1_set1_pen3_N4 Neutral Gray.svg"]) </br>
