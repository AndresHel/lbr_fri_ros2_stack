from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ld = LaunchDescription()
    
    bringup_dir = get_package_share_directory("lbr_bringup")
    hardware_launch = os.path.join(bringup_dir, "launch", "hardware.launch.py")

    robot_left = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(hardware_launch),
        launch_arguments={
            "ctrl": "lbr_joint_position_command_controller",
            "model": "iiwa7",
            "robot_name": "iiwa_left",
            "sys_cfg": "lbr_system_config_left.yaml",
        }.items(),
    )

    robot_right = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(hardware_launch),
        launch_arguments={
            "ctrl": "lbr_joint_position_command_controller",
            "model": "iiwa7",
            "robot_name": "iiwa_right",
            "sys_cfg": "lbr_system_config_right.yaml",
        }.items(),
    )

    ld.add_action(robot_left)
    ld.add_action(robot_right)
    return ld