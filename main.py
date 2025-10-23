import serial
import subprocess
from tqdm import tqdm 

class AutoPen():
    """
    NOTE
    the position where the pen is is always considered to be 0,0 by default.
    
    """
    def __init__(self,device_location:str='/dev/ttyACM0',default_speed:float=2000):
        self.ser = serial.Serial(device_location, 115200, timeout=1)
        self.current_speed = default_speed
        self.default_speed = default_speed

        #setup 
        self.set_speed(self.default_speed)
        self.set_absolute_coordinate_mode()
        self._current_location_as_x0y0()
        self.set_pen_height(0)

    def send_gcode(self,command:str) -> None:
        """
        sends commands to the device using gcodes and waits for confirmation 
        """
        self.ser.write((command + '\n').encode())
        while True:
            line = self.ser.readline().decode().strip()
            if line.lower() == 'ok':
                break
    
    def close(self) -> None:
        """
        close connection
        """
        self.ser.close()


    def _current_location_as_x0y0(self) -> None:
        """
        saves the current position of the writing head as x=0,y=0.
        So all absolute movements are relative to this point
        """

        self.send_gcode("G92 X0Y0")

    def set_absolute_coordinate_mode(self) -> None:
        """
        basically sees everything relative from the x=0,y=0 position
        """
        self.send_gcode("G90")
        self.is_absolute_coordinate_mode = True 
    
    def set_relative_coordinate_mode(self) -> None:
        """
        basically sees the last position as the x=0,y=0 position and all movements are 
        relative to the last position
        """
        self.send_gcode("G91")

        self.is_absolute_coordinate_mode = False 

    def set_pen_height(self,height:float) -> None:
        """
        0 is all the way up
        9 is all the way down (with some space left so the motor doesn't run into the metal)

        I put it so it always moves in absolute coordinate mode, otherwise you move the height of the pen relative to it's previous position.
        
        NOTE: 
        (turning the iDraw H A3 Pen Plotter off and then on again will reset the height of the pen to position 0) 
        """
        assert height >= 0 
        assert height <= 9

        if(self.is_absolute_coordinate_mode):
            self.send_gcode(f"G00 Z{height}")
        else:
            self.set_absolute_coordinate_mode()
            self.send_gcode(f"G00 Z{height}")
            self.set_relative_coordinate_mode()

    def set_speed(self,speed:float) -> None:
        """
        set the speed of any variable speed opperation
        """
        assert speed >= 50 
        assert speed <= 2500

        self.send_gcode(f"F{speed}")

    def move_xy_constant_speed(self,x:float,y:float) -> None:
        """
        x is horizantal moving (in milimeters)
        y is verticle moving (in milimeters)

        G00 (as used in self.move_xy) uses constant speed,
        so is not subjected to the set speed
        """

        self.send_gcode(f"G00 X{x} Y{y}")


    def move_xy_variable_speed(self,x:float,y:float,speed:float=None,update_current_speed:bool=True) -> None:
        """
        x is horizantal moving (in milimeters)
        y is verticle moving (in milimeters)

        speed is goes from 50 to 2500, where 50 is slow and 2500 is fast
        update_current_speed will make it that next time you use move_xy_variable_speed that the new speed will be used
        otherwise it will go back to the previous speed.
        """
        if(not (speed is None) and speed != self.current_speed):
            self.set_speed(speed)

            if(not update_current_speed):
                #return to previous current speed after movement 
                self.set_speed(self.current_speed) 
            else:
                self.current_speed = speed 

        self.send_gcode(f"G01 X{x} Y{y}")
        

    def _set_scale_to_mm(self) -> None:
        """
        if for whatever reason it is in inches this will put it to milimeters. (default seems to always be milimeters)
        """
        self.send_gcode("G21")


    def arc_clock_wise(self,x:float,y:float,I:float,J:float) -> None:
        """
        x,y are the end point of the arc (note the end point needs to be a valid pont on the arc)

        I,J are the arc's center point coordinates relative to the starting coordinates  (when starting to draw the arc)

        NOTE that in absolute mode x,y is the absolute end point of the arc and I and J is the center point of the arc relative 
        to the starting coordinates from which you start drawing the arc.
 
        """

        self.send_gcode(f"G02 X{x} Y{y} I{I} J{J}")

    def arc_counter_clock_wise(self,x:float,y:float,I:float,J:float) -> None:
        """
        x,y are the end point of the arc (note the end point needs to be a valid pont on the arc)

        I,J are the arc's center point coordinates relative to the starting coordinates (when starting to draw the arc)
 
        NOTE that in absolute mode x,y is the absolute end point of the arc and I and J is the center point of the arc relative 
        to the starting coordinates from which you start drawing the arc.

        """

        self.send_gcode(f"G03 X{x} Y{y} I{I} J{J}")



def convert_svg_to_gcode_vpype(path_input_file:str,path_output_file:str):
    """
    NOTE that, "vpype converts everything curvy (circles, bezier curves, etc.) to lines made of small segments.
      vpype does import metadata such stroke and fill color, stroke width, etc., it only makes partial use of them and does not aim to maintain a 
      full consistency with the SVG specification"


    usage example:
        convert_svg_to_gcode_vpype("./input.svg","./output.gcode")

    """
    subprocess.run(["vpype", "--config", "vpype-settings.toml","read", path_input_file, "gwrite", "--profile", "idrawv2",path_output_file])



def execute_raw_gcode_from_file(pen:AutoPen,path_gcode_file:str) -> None:
    """
    this will read and execute the gcode from a file.

    if return_to_start is true it will return to x=0 and y=0 when it's done.

    """
    commands = []
    
    #read and preprocess
    with open(path_gcode_file, 'r') as file:
        for line in file:
            command = line.strip().split(";")[0]

            if(not len(command) == 0):
                commands.append(command)

    #execute 
    for command in tqdm(commands,ascii=True,total=len(commands)):
            
        pen.send_gcode(command)


def plot_svg(pen:AutoPen,image_path:str,temp_gcode_file_path:str="./output.gcode") -> None:
    """
    will make the writing robot draw the svg, (atleast a linearized version of it, because vpyp linearized when converting to gcode)
    """

    convert_svg_to_gcode_vpype(image_path,temp_gcode_file_path)
    execute_raw_gcode_from_file(pen,temp_gcode_file_path)


def multilayer_svg(pen:AutoPen,image_paths:list[str],temp_gcode_file_path:str="./output.gcode"):
        """
        idea is that you give multiple paths to all the different layers, each image should  be an svg
        """
        for path in image_paths:
            while(True):
                user_input = input("continue? Type 'y' to continue\n")
                if(user_input == "y"):
                    break 
            
            plot_svg(pen,path,temp_gcode_file_path)

        

if __name__ == "__main__":        
    pen = AutoPen()
    multilayer_svg(pen,["multilayer_image/green_layer_resized.svg","multilayer_image/red_layer_resized.svg","multilayer_image/blue_layer_resized.svg"])


