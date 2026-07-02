
"""
from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.actions import TimerAction
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration
from lbr_bringup.description import LBRDescriptionMixin
from lbr_bringup.ros2_control import LBRROS2ControlMixin


def generate_launch_description() -> LaunchDescription:
    ld = LaunchDescription()

    # launch arguments
    ld.add_action(LBRDescriptionMixin.arg_model())
    ld.add_action(LBRDescriptionMixin.arg_robot_name())
    ld.add_action(LBRROS2ControlMixin.arg_sys_cfg_pkg())
    ld.add_action(LBRROS2ControlMixin.arg_sys_cfg())
    ld.add_action(LBRROS2ControlMixin.arg_ctrl_cfg_pkg())
    ld.add_action(LBRROS2ControlMixin.arg_ctrl_cfg())
    ld.add_action(LBRROS2ControlMixin.arg_ctrl())

    robot_name = LaunchConfiguration("robot_name") 
    # robot description
    robot_description = LBRDescriptionMixin.param_robot_description(mode="hardware")

    # robot state publisher
    robot_state_publisher = LBRROS2ControlMixin.node_robot_state_publisher(
        robot_description=robot_description, robot_name=robot_name, use_sim_time=False
    )
    ld.add_action(robot_state_publisher)

    # ros2 control node
    ros2_control_node = LBRROS2ControlMixin.node_ros2_control(
        robot_name=robot_name, use_sim_time=False, robot_description=robot_description
    )
    ld.add_action(ros2_control_node)

    controller_manager = LaunchConfiguration("controller_manager", default="controller_manager")




    # joint state broad caster and controller on ros2 control node start
    joint_state_broadcaster = LBRROS2ControlMixin.node_controller_spawner(
        robot_name=robot_name,
        controller="joint_state_broadcaster",
        controller_manager=controller_manager,
    )
    force_torque_broadcaster = LBRROS2ControlMixin.node_controller_spawner(
        robot_name=robot_name,
        controller="force_torque_broadcaster"
    )
    lbr_state_broadcaster = LBRROS2ControlMixin.node_controller_spawner(
        robot_name=robot_name,
        controller="lbr_state_broadcaster"
    )
    controller = LBRROS2ControlMixin.node_controller_spawner(
        robot_name=robot_name,
        controller=LaunchConfiguration("ctrl")
    )

    

    controller_event_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=ros2_control_node,
            on_start=[
                joint_state_broadcaster,
                force_torque_broadcaster,
                lbr_state_broadcaster,
                controller,
            ],
        )
    )
    ld.add_action(controller_event_handler)




    return ld
"""

from launch import LaunchDescription
from launch.actions import OpaqueFunction, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.launch_context import LaunchContext
from launch.substitutions import LaunchConfiguration
from lbr_bringup.description import LBRDescriptionMixin
from lbr_bringup.ros2_control import LBRROS2ControlMixin


def launch_setup(context: LaunchContext, *args, **kwargs):
    # Resolve to plain strings NOW, while this include's context is active.
    # This avoids the race condition where concurrently-included launch
    # descriptions overwrite each other's LaunchConfiguration values by the
    # time deferred (event-handler-triggered) actions actually execute.
    robot_name = LaunchConfiguration("robot_name").perform(context)
    controller_manager = LaunchConfiguration(
        "controller_manager", default="controller_manager"
    ).perform(context)
    ctrl = LaunchConfiguration("ctrl").perform(context)

    robot_description = LBRDescriptionMixin.param_robot_description(mode="hardware")

    robot_state_publisher = LBRROS2ControlMixin.node_robot_state_publisher(
        robot_description=robot_description, robot_name=robot_name, use_sim_time=False
    )

    ros2_control_node = LBRROS2ControlMixin.node_ros2_control(
        robot_name=robot_name, use_sim_time=False, robot_description=robot_description
    )

    joint_state_broadcaster = LBRROS2ControlMixin.node_controller_spawner(
        robot_name=robot_name,
        controller="joint_state_broadcaster",
        controller_manager=controller_manager,
        namespace="",
    )
    force_torque_broadcaster = LBRROS2ControlMixin.node_controller_spawner(
        robot_name=robot_name,
        controller="force_torque_broadcaster",
        controller_manager=controller_manager,
        namespace="",
    )
    lbr_state_broadcaster = LBRROS2ControlMixin.node_controller_spawner(
        robot_name=robot_name,
        controller="lbr_state_broadcaster",
        controller_manager=controller_manager,
        namespace="",
    )
    controller = LBRROS2ControlMixin.node_controller_spawner(
        robot_name=robot_name,
        controller=ctrl,
        controller_manager=controller_manager,
        namespace="",
    )

    controller_event_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=ros2_control_node,
            on_start=[
                joint_state_broadcaster,
                force_torque_broadcaster,
                lbr_state_broadcaster,
                controller,
            ],
        )
    )

    return [
        robot_state_publisher,
        ros2_control_node,
        controller_event_handler,
    ]


def generate_launch_description() -> LaunchDescription:
    ld = LaunchDescription()

    ld.add_action(LBRDescriptionMixin.arg_model())
    ld.add_action(LBRDescriptionMixin.arg_robot_name())
    ld.add_action(LBRROS2ControlMixin.arg_sys_cfg_pkg())
    ld.add_action(LBRROS2ControlMixin.arg_sys_cfg())
    ld.add_action(LBRROS2ControlMixin.arg_ctrl_cfg_pkg())
    ld.add_action(LBRROS2ControlMixin.arg_ctrl_cfg())
    ld.add_action(LBRROS2ControlMixin.arg_ctrl())

    ld.add_action(OpaqueFunction(function=launch_setup))

    return ld