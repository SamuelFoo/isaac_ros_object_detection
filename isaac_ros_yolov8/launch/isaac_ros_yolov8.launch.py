import os

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def evaluate_launch(context, *args, **kwargs):
    param_path = LaunchConfiguration("param_path").perform(context)

    with open(param_path, "r") as f:
        yaml_params = yaml.safe_load(f)["/**"]["ros__parameters"]
    yaml_params: dict

    tensor_rt_params = {
        "input_binding_names": '["images"]',
        "output_binding_names": '["output0"]',
        "force_engine_update": "False",
        "image_mean": "[0.0, 0.0, 0.0]",
        "image_stddev": "[1.0, 1.0, 1.0]",
        "confidence_threshold": "0.25",
        "nms_threshold": "0.45",
    }
    tensor_rt_params = tensor_rt_params | yaml_params

    return [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [
                    os.path.join(
                        get_package_share_directory("isaac_ros_yolov8"),
                        "launch",
                    ),
                    "/yolov8_tensor_rt.launch.py",
                ]
            ),
            launch_arguments=tensor_rt_params.items(),
        )
    ]


def generate_launch_description():
    launch_args = [
        DeclareLaunchArgument(
            "param_path",
            default_value=PathJoinSubstitution(
                [
                    FindPackageShare("isaac_ros_yolov8"),
                    "config",
                    "auv4_orin.yaml",
                ]
            ),
            description="Path to parameter file",
        ),
    ]

    return LaunchDescription(
        launch_args
        + [
            OpaqueFunction(function=evaluate_launch),
            Node(
                package="isaac_ros_yolov8",
                executable="isaac_ros_yolov8_visualizer.py",
                name="yolov8_visualizer",
            ),
        ]
    )
