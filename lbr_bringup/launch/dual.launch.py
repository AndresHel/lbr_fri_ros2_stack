

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
            "sys_cfg": "ros2_control/lbr_system_config_left.yaml",
            "ctrl_cfg": "ros2_control/lbr_controllers_left.yaml",
            "controller_manager": "iiwa_left/controller_manager",
        }.items(),
    )

    robot_right = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(hardware_launch),
        launch_arguments={
            "ctrl": "lbr_joint_position_command_controller",
            "model": "iiwa7",
            "robot_name": "iiwa_right",
            "sys_cfg": "ros2_control/lbr_system_config_right.yaml",
            "ctrl_cfg": "ros2_control/lbr_controllers_right.yaml",
            "controller_manager": "iiwa_right/controller_manager",
        }.items(),
    )

    ld.add_action(robot_left)
    ld.add_action(robot_right)
    return ld


"""
from launch import LaunchDescription
from launch.actions import GroupAction
from launch_ros.actions import PushRosNamespace
from lbr_bringup.description import LBRDescriptionMixin
from lbr_bringup.ros2_control import LBRROS2ControlMixin


def arm_group(robot_name, ctrl_cfg, sys_cfg):
    robot_description = LBRDescriptionMixin.param_robot_description(mode="hardware")

    return GroupAction(
        actions=[
            PushRosNamespace(robot_name),
            LBRROS2ControlMixin.node_robot_state_publisher(
                robot_description=robot_description,
                robot_name=robot_name,
                use_sim_time=False,
            ),
            LBRROS2ControlMixin.node_ros2_control(
                robot_name=robot_name,
                use_sim_time=False,
                robot_description=robot_description,
            ),
            LBRROS2ControlMixin.node_controller_spawner(
                robot_name=robot_name,
                controller="joint_state_broadcaster",
                controller_manager="controller_manager",
            ),
            LBRROS2ControlMixin.node_controller_spawner(
                robot_name=robot_name,
                controller="force_torque_broadcaster",
                controller_manager="controller_manager",
            ),
            LBRROS2ControlMixin.node_controller_spawner(
                robot_name=robot_name,
                controller="lbr_state_broadcaster",
                controller_manager="controller_manager",
            ),
            LBRROS2ControlMixin.node_controller_spawner(
                robot_name=robot_name,
                controller="lbr_joint_position_command_controller",
                controller_manager="controller_manager",
            ),
        ],
    )


def generate_launch_description():
    ld = LaunchDescription()

    ld.add_action(
        arm_group(
            "iiwa_left",
            "ros2_control/lbr_controllers_left.yaml",
            "ros2_control/lbr_system_config_left.yaml",
        )
    )
    ld.add_action(
        arm_group(
            "iiwa_right",
            "ros2_control/lbr_controllers_right.yaml",
            "ros2_control/lbr_system_config_right.yaml",
        )
    )

    return ld  """