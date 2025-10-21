#pragma once

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "sensor_msgs/msg/compressed_image.hpp"
#include "std_msgs/msg/float32.hpp"
#include "std_msgs/msg/string.hpp"
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>
#include <sensor_msgs/image_encodings.hpp>
#include <boost/filesystem.hpp>
#include <iostream>
#include <string>
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/int32.hpp>
#include <std_msgs/msg/string.hpp>
#include <sensor_msgs/msg/compressed_image.hpp>
#include <sensor_msgs/msg/imu.hpp>
#include <cv_bridge/cv_bridge.h>
#include "ros2_aruco_interfaces/msg/aruco_markers.hpp"

class Ros2Node : public rclcpp::Node
{
public:
    Ros2Node();
    ~Ros2Node();

    cv::Mat getRosMsg();
    std::string getDepth();
    std::string getSonar();
    std::string getIMU();
    std::string getOrin();
    std::string getBag();

private:
    cv::Mat cv_ptr;
    float depth;
    std::string sonar;
    std::string imu;
    std::string orin;
    std::string device;
    std::string bag;

    rclcpp::Subscription<sensor_msgs::msg::CompressedImage>::SharedPtr cam_sub_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sonar_sub_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr orin_sub_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr bag_sub_;
    rclcpp::Subscription<std_msgs::msg::Float32>::SharedPtr depth_sub_;
    rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr imu_sub_;
    rclcpp::Subscription<ros2_aruco_interfaces::msg::ArucoMarkers>::SharedPtr tag_sub_;
    rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr tag_id_pub_;

    void cam_callback(const sensor_msgs::msg::CompressedImage::SharedPtr msg);
    void depth_callback(const std_msgs::msg::Float32::SharedPtr msg);
    void sonar_callback(const std_msgs::msg::String::SharedPtr msg);
    void bag_callback(const std_msgs::msg::String::SharedPtr msg);
    void orin_callback(const std_msgs::msg::String::SharedPtr msg);
    void imu_callback(const sensor_msgs::msg::Imu::SharedPtr msg);
    void tag_callback(const ros2_aruco_interfaces::msg::ArucoMarkers::SharedPtr msg);
};