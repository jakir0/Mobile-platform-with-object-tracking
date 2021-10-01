# Automatic mobile platform navigation system using object tracking
### About
* Developed for Raspberry Pi 3 B+
* Camera module: Raspberry Pi Camera HD v2 
* Powered by: 4 x 18650 batteries and 2 x [Pololu D24V22F5](https://www.pololu.com/product/2858)
* 2 DC motors: [Pololu 1125](https://www.pololu.com/product/1125) driven by [Pololu DRV8835](https://www.pololu.com/product/2135) with [drv8835-motor-driver-rpi python library](https://github.com/pololu/drv8835-motor-driver-rpi)
* Tracking algorthm based on color of the tracked object utilizing OpenCV library
### How to use
After starting script you will see 5 widows pop up

1. Hue - Hue channel of video feed
2. Saturation - Saturation channel of video feed
3. Value - Value channel of video feed
4. Closing result of bitwise AND operation between channels
5. Tracking video feed with circle enclosing tracked object

Now set-up takes place
1. Set sliders of every channel in positions where in "Closing" window only tracked object is seen.
1. Put tracked object in desirable distance in front of the platform(platform will try to reach this distance when main loop starts)
1. Press ESC key to start main loop 

### Video presentation of the platform following a red ball
https://user-images.githubusercontent.com/83252838/135636763-d98e42e5-d137-4392-baf1-c16db09f7ae5.mp4

### The appearance of the mobile platform
![image](https://user-images.githubusercontent.com/83252838/135641375-dffb1245-7889-4839-ab46-f37e1718d696.png)
![image](https://user-images.githubusercontent.com/83252838/135641411-be3b7131-6bdf-4d3e-bbe1-61f83264ce7c.png)
![image](https://user-images.githubusercontent.com/83252838/135641450-524b8e44-6e74-4aa7-af29-53d419eff6af.png)
![image](https://user-images.githubusercontent.com/83252838/135641467-eebe560a-79df-4161-a01f-232c723e6dfb.png)

### Connections diagram
![image](https://user-images.githubusercontent.com/83252838/135639348-e1447958-608a-4421-9ca7-7529c7108a1b.png)
