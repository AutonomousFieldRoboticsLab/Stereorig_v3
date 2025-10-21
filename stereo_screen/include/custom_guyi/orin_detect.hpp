#ifndef ORIN_DETECT_HPP
#define ORIN_DETECT_HPP

#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

class orin_detect : public rclcpp::Node
{
public:
    orin_detect();

private:
    void timer_callback();
    std::string jetsonCheck(std::string device);

    std::string device;
    std::string orin;
    float depth;
    double timer_period;

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

#endif
