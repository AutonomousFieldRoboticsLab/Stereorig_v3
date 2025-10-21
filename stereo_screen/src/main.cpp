#include <QApplication>
#include <signal.h>
#include "custom_guyi/orin_detect.hpp"
#include "custom_guyi/ros2node.hpp"
#include "custom_guyi/main_gui.hpp"

static void siginthandler(int /*param*/)
{
    QApplication::quit();
}

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);

    // Initialize ROS 2
    rclcpp::init(argc, argv);

    auto ros2_node = std::make_shared<Ros2Node>();
    auto gui_app = std::make_shared<MainGUI>(ros2_node);

    app.processEvents();
    gui_app->show();

    rclcpp::executors::MultiThreadedExecutor exec;
    exec.add_node(ros2_node);

    auto orin_detect_node = std::make_shared<orin_detect>();
    exec.add_node(orin_detect_node);

    while (rclcpp::ok())
    {
        exec.spin_some();
        app.processEvents();
    }

    signal(SIGINT, siginthandler);

    exec.remove_node(ros2_node);
    exec.remove_node(orin_detect_node);
    rclcpp::shutdown();

    return 0;
}
