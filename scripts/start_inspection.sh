xterm -geometry 80x5+0+130 -e "/opt/ros/indigo/bin/roslaunch turtlebot_bringup minimal.launch" &
sleep 7s
xterm -geometry 80x5+0+230 -e "/opt/ros/indigo/bin/roslaunch turtlebot_bringup 3dsensor.launch" &
sleep 10s
xterm -geometry 80x5+0+330 -e "/opt/ros/indigo/bin/rqt -s kobuki_dashboard" &
sleep 5s
xterm -geometry 80x5+0+430 -e "/opt/ros/indigo/bin/roslaunch turtlebot_navigation amcl_demo.launch map_file:=/home/demulab/map/canada_arena.yaml" &
sleep 5s
xterm -geometry 80x5+0+530 -e "/opt/ros/indigo/bin/roslaunch turtlebot_rviz_launchers view_navigation.launch" &
sleep 5s
xterm -geometry 80x5+0+130 -e "/opt/ros/indigo/bin/rosrun inspect EInspection.py" &
