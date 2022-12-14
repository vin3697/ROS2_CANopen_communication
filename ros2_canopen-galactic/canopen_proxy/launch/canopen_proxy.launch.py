# Copyright 2022 Christoph Hellmann Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
import launch
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    
    #launching slave node
    slave_eds_path = os.path.join(
                    get_package_share_directory("canopen_proxy"), "config", "proxy", "simple.eds"
                )

    #entire launch file is launched
    proxy_device = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("canopen_mock_slave"), "launch"
                ),
                "/basic_slave.launch.py",
            ]
        ),
        launch_arguments={
            "node_id": "2", 
            "node_name": "proxy_device",
            "slave_config": slave_eds_path,
            }.items(),
    )

    #launching master node 
    master_bin_path = os.path.join(
                get_package_share_directory("canopen_proxy"),
                "config",
                "proxy",
                "master.bin",
            )     
    if not os.path.exists(master_bin_path):
        master_bin_path = ""            
    device_container = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("canopen_core"), "launch"),
                "/canopen.launch.py",
            ]
        ),
        launch_arguments={
            "master_config": os.path.join(
                get_package_share_directory("canopen_proxy"),
                "config",
                "proxy",
                "master.dcf",
            ),
            "master_bin": master_bin_path,
            "bus_config": os.path.join(
                get_package_share_directory("canopen_proxy"),
                "config",
                "proxy",
                "bus.yml",#folder path
            ),
            "can_interface_name": "can0",
        }.items(),
    )

    return LaunchDescription([proxy_device, device_container])
