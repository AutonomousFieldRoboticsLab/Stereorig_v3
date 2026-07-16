# -----------------------------------------------------------------------------
# Copyright 2022 Bernd Pfrommer <bernd.pfrommer@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration as LaunchConfig
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


example_parameters = {
    'blackfly_s': {
        'pixel_format': 'BGR8',
        'debug': False,
        'compute_brightness': False,
        'adjust_timestamp': True,
        'dump_node_map': False,

        # set parameters defined in blackfly_s.yaml
        'gain_auto': 'Continuous',
        'exposure_auto': 'Continuous',

        # to use a user set, do this:
        'user_set_selector': 'UserSet0',
        'user_set_load': 'Yes',

        # These are useful for GigE cameras
        # 'device_link_throughput_limit': 380000000,
        # 'gev_scps_packet_size': 9000,

        # ---- to reduce the sensor width and shift the crop
        # 'image_width': 1408,
        # 'image_height': 1080,
        # 'offset_x': 16,
        # 'offset_y': 0,
        # 'binning_x': 1,
        # 'binning_y': 1,
        # 'connect_while_subscribed': True,

        'frame_rate_auto': 'Off',
        'frame_rate': 20.0,
        'frame_rate_enable': True,
        'buffer_queue_size': 10,
        'trigger_mode': 'Off',

        'chunk_mode_active': True,
        'chunk_selector_frame_id': 'FrameID',
        'chunk_enable_frame_id': True,
        'chunk_selector_exposure_time': 'ExposureTime',
        'chunk_enable_exposure_time': True,
        'chunk_selector_gain': 'Gain',
        'chunk_enable_gain': True,
        'chunk_selector_timestamp': 'Timestamp',
        'chunk_enable_timestamp': True,

        'adc_bit_depth': 'Bit12',
    },

    'blackfly': {
        'debug': False,
        'dump_node_map': False,
        'gain_auto': 'Continuous',
        'pixel_format': 'BayerRG8',
        'exposure_auto': 'Continuous',
        'frame_rate_auto': 'Off',
        'frame_rate': 40.0,
        'frame_rate_enable': True,
        'buffer_queue_size': 10,
        'trigger_mode': 'Off',

        # 'stream_buffer_handling_mode': 'NewestFirst',
        # 'multicast_monitor_mode': False
    },

    'chameleon': {
        'debug': False,
        'compute_brightness': False,
        'dump_node_map': False,

        # set parameters defined in chameleon.yaml
        'gain_auto': 'Continuous',
        'exposure_auto': 'Continuous',
        'offset_x': 0,
        'offset_y': 0,
        'image_width': 2048,
        'image_height': 1536,
        'pixel_format': 'RGB8',
        'frame_rate_continous': True,
        'frame_rate': 100.0,
        'trigger_mode': 'Off',

        'chunk_mode_active': True,
        'chunk_selector_frame_id': 'FrameID',
        'chunk_enable_frame_id': True,
        'chunk_selector_exposure_time': 'ExposureTime',
        'chunk_enable_exposure_time': True,
        'chunk_selector_gain': 'Gain',
        'chunk_enable_gain': True,
        'chunk_selector_timestamp': 'Timestamp',
        'chunk_enable_timestamp': True,
    },

    'grasshopper': {
        'debug': False,
        'compute_brightness': False,
        'dump_node_map': False,

        # set parameters defined in grasshopper.yaml
        'gain_auto': 'Continuous',
        'exposure_auto': 'Continuous',
        'frame_rate_auto': 'Off',
        'frame_rate': 100.0,
        'trigger_mode': 'Off',

        'chunk_mode_active': True,
        'chunk_selector_frame_id': 'FrameID',
        'chunk_enable_frame_id': True,
        'chunk_selector_exposure_time': 'ExposureTime',
        'chunk_enable_exposure_time': True,
        'chunk_selector_gain': 'Gain',
        'chunk_enable_gain': True,
        'chunk_selector_timestamp': 'Timestamp',
        'chunk_enable_timestamp': True,
    },

    'flir_ax5': {
        'debug': False,
        'compute_brightness': False,
        'adjust_timestamp': False,
        'dump_node_map': False,

        # --- Set parameters defined in flir_ax5.yaml
        'pixel_format': 'Mono8',
        'gev_scps_packet_size': 576,
        'image_width': 640,
        'image_height': 512,
        'offset_x': 0,
        'offset_y': 0,
        'sensor_gain_mode': 'HighGainMode',
        'nuc_mode': 'Automatic',
        'sensor_dde_mode': 'Automatic',
        'sensor_video_standard': 'NTSC30HZ',

        # valid values:
        # "PlateauHistogram"
        # "OnceBright"
        # "AutoBright"
        # "Manual"
        # "Linear"
        'image_adjust_method': 'PlateauHistogram',
        'video_orientation': 'Normal',
    },
}


def launch_setup(context, *args, **kwargs):
    """Launch camera driver node."""

    parameter_file = LaunchConfig('parameter_file').perform(context)
    camera_type = LaunchConfig('camera_type').perform(context)

    if not parameter_file:
        parameter_file = PathJoinSubstitution(
            [
                FindPackageShare('spinnaker_camera_driver'),
                'config',
                camera_type + '.yaml',
            ]
        )

    if camera_type not in example_parameters:
        raise Exception(
            'no example parameters available for type ' + camera_type
        )

    # Common parameters supplied by both stereorig launch files.
    # This dictionary is applied after example_parameters, so these values
    # override the camera-type defaults.
    camera_overrides = {
        'debug': ParameterValue(
            LaunchConfig('debug'),
            value_type=bool,
        ),
        'compute_brightness': ParameterValue(
            LaunchConfig('compute_brightness'),
            value_type=bool,
        ),
        'adjust_timestamp': ParameterValue(
            LaunchConfig('adjust_timestamp'),
            value_type=bool,
        ),
        'dump_node_map': ParameterValue(
            LaunchConfig('dump_node_map'),
            value_type=bool,
        ),

        'gain_auto': ParameterValue(
            LaunchConfig('gain_auto'),
            value_type=str,
        ),
        'exposure_auto': ParameterValue(
            LaunchConfig('exposure_auto'),
            value_type=str,
        ),
        'user_set_selector': ParameterValue(
            LaunchConfig('user_set_selector'),
            value_type=str,
        ),
        'user_set_load': ParameterValue(
            LaunchConfig('user_set_load'),
            value_type=str,
        ),

        'frame_rate_auto': ParameterValue(
            LaunchConfig('frame_rate_auto'),
            value_type=str,
        ),
        'frame_rate': ParameterValue(
            LaunchConfig('frame_rate'),
            value_type=float,
        ),
        'frame_rate_enable': ParameterValue(
            LaunchConfig('frame_rate_enable'),
            value_type=bool,
        ),
        'buffer_queue_size': ParameterValue(
            LaunchConfig('buffer_queue_size'),
            value_type=int,
        ),
        'trigger_mode': ParameterValue(
            LaunchConfig('trigger_mode'),
            value_type=str,
        ),

        'chunk_mode_active': ParameterValue(
            LaunchConfig('chunk_mode_active'),
            value_type=bool,
        ),
        'chunk_selector_frame_id': ParameterValue(
            LaunchConfig('chunk_selector_frame_id'),
            value_type=str,
        ),
        'chunk_enable_frame_id': ParameterValue(
            LaunchConfig('chunk_enable_frame_id'),
            value_type=bool,
        ),
        'chunk_selector_exposure_time': ParameterValue(
            LaunchConfig('chunk_selector_exposure_time'),
            value_type=str,
        ),
        'chunk_enable_exposure_time': ParameterValue(
            LaunchConfig('chunk_enable_exposure_time'),
            value_type=bool,
        ),
        'chunk_selector_gain': ParameterValue(
            LaunchConfig('chunk_selector_gain'),
            value_type=str,
        ),
        'chunk_enable_gain': ParameterValue(
            LaunchConfig('chunk_enable_gain'),
            value_type=bool,
        ),
        'chunk_selector_timestamp': ParameterValue(
            LaunchConfig('chunk_selector_timestamp'),
            value_type=str,
        ),
        'chunk_enable_timestamp': ParameterValue(
            LaunchConfig('chunk_enable_timestamp'),
            value_type=bool,
        ),

        'ffmpeg_image_transport.encoding': 'hevc_nvenc',
        'parameter_file': parameter_file,
        'serial_number': [LaunchConfig('serial')],
    }

    # Primary-only and Secondary-only arguments have empty defaults.
    # Add a parameter only when the parent launch supplied a value.
    optional_string_parameters = (
        'line1_selector',
        'line1_linemode',
        'line2_selector',
        'trigger_selector',
        'trigger_source',
        'trigger_overlap',
    )

    for parameter_name in optional_string_parameters:
        parameter_value = LaunchConfig(parameter_name).perform(context)

        if parameter_value:
            camera_overrides[parameter_name] = parameter_value

    line2_v33enable = LaunchConfig(
    'line2_v33enable'
    ).perform(context)

    if line2_v33enable:
        camera_overrides['line2_v33enable'] = ParameterValue(
            LaunchConfig('line2_v33enable'),
            value_type=bool,
        )

    node = Node(
        package='spinnaker_camera_driver',
        executable='camera_driver_node',
        output='screen',
        name=[LaunchConfig('camera_name')],
        parameters=[
            example_parameters[camera_type],
            camera_overrides,
        ],
        remappings=[
            ('~/control', '/exposure_control/control'),
        ],
    )

    return [node]


def generate_launch_description():
    """Create composable node by calling opaque function."""

    return LaunchDescription(
        [
            LaunchArg(
                'camera_name',
                default_value=['flir_camera'],
                description='camera name (ros node name)',
            ),
            LaunchArg(
                'camera_type',
                default_value='blackfly_s',
                description='type of camera (blackfly_s, chameleon...)',
            ),
            LaunchArg(
                'serial',
                default_value="'20435008'",
                description='FLIR serial number of camera (in quotes!!)',
            ),
            LaunchArg(
                'parameter_file',
                default_value='',
                description=(
                    'path to ros parameter definition file '
                    '(override camera type)'
                ),
            ),

            # Common arguments supplied by both stereorig launch files.
            LaunchArg('debug'),
            LaunchArg('compute_brightness'),
            LaunchArg('adjust_timestamp'),
            LaunchArg('dump_node_map'),

            LaunchArg('gain_auto'),
            LaunchArg('exposure_auto'),
            LaunchArg('user_set_selector'),
            LaunchArg('user_set_load'),

            LaunchArg('frame_rate_auto'),
            LaunchArg('frame_rate'),
            LaunchArg('frame_rate_enable'),
            LaunchArg('buffer_queue_size'),
            LaunchArg('trigger_mode'),

            LaunchArg('chunk_mode_active'),
            LaunchArg('chunk_selector_frame_id'),
            LaunchArg('chunk_enable_frame_id'),
            LaunchArg('chunk_selector_exposure_time'),
            LaunchArg('chunk_enable_exposure_time'),
            LaunchArg('chunk_selector_gain'),
            LaunchArg('chunk_enable_gain'),
            LaunchArg('chunk_selector_timestamp'),
            LaunchArg('chunk_enable_timestamp'),

            # Primary-only GPIO output settings.
            # These remain empty on the Secondary Jetson.
            LaunchArg(
                'line1_selector',
                default_value='',
            ),
            LaunchArg(
                'line1_linemode',
                default_value='',
            ),
            LaunchArg(
                'line2_selector',
                default_value='',
            ),
            LaunchArg(
                'line2_v33enable',
                default_value='',
            ),

            # Secondary-only external-trigger settings.
            # These remain empty on the Primary Jetson.
            LaunchArg(
                'trigger_selector',
                default_value='',
            ),
            LaunchArg(
                'trigger_source',
                default_value='',
            ),
            LaunchArg(
                'trigger_overlap',
                default_value='',
            ),

            OpaqueFunction(function=launch_setup),
        ]
    )