## Execution

### Build docker image
Run command

`dts devel build -f `

### Run docker container on PC with access to ROS on duckiebot
Run command

`docker  run -it --net host -e ROS_MASTER_URI=http://<host_ip>:11311/ -e ROS_IP=<duckiebot_ip> duckietown/duckietown_colordetector_ros:v2-amd64`

Replace `<host_ip>` and `<duckiebot_ip>` with the IP address of your PC and your duckiebot. You can check the IP address with command `ifconfig`. 

### Set color to detect
Open a container connected to the duckbot with command

`dts start_gui_tools <robot_name>`

Replace `<robot_name>` with name of your duckiebot.

Change rosparameter to "red" or "yellow" with command

`rosparam set /colordetector/color <value>`

Replace `<robot_name>` with name of your duckiebot. Replace `<value>` with "red" or "yellow".

### Check result
Open a container connected to the duckbot with command

`dts start_gui_tools <robot_name>`

Replace `<robot_name>` with name of your duckiebot.

Run command 

`rqt_image_view`

Check topic

`/colordetector/image/compressed`
