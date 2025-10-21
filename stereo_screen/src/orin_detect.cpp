#include "custom_guyi/orin_detect.hpp"

orin_detect::orin_detect()
    : rclcpp::Node("orin_detect"), depth(0.0f), timer_period(30.0)
{
    this->declare_parameter<std::string>("device", "");
    this->get_parameter("device", device);
    
    orin = "Not Active";
    publisher_ = this->create_publisher<std_msgs::msg::String>("orin", 10);
    timer_ = this->create_wall_timer(
        std::chrono::duration<double>(timer_period),
        std::bind(&orin_detect::timer_callback, this)
    );
}

std::string orin_detect::jetsonCheck(std::string device) {
    if (device == "jetson_1") {
        int x = system("ping -c1 -s1 192.168.0.100 > /dev/null 2>&1");
        return (x == 0) ? "Active" : "Not Active";
    } else if (device == "jetson_2") {
        int x = system("ping -c1 -s1 192.168.0.150 > /dev/null 2>&1");
        return (x == 0) ? "Active" : "Not Active";
    } else {
        return "Unknown Device";
    }
}

void orin_detect::timer_callback() {
    orin = jetsonCheck(device);
    auto message = std_msgs::msg::String();
    message.data = orin;
    publisher_->publish(message);
}
