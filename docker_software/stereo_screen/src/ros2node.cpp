#include "custom_guyi/ros2node.hpp"

Ros2Node::Ros2Node()
  : Node("ros2_node"), depth(0.0f)
{
    imu = "Not Active";
    orin = "Not Active";
    sonar = "Not Active";
    bag = "Not Active";
    std::string device = "null";

    declare_parameter<std::string>("device", "null");
    get_parameter("device", device);

    declare_parameter<std::string>("cam_topic", "flir_camera/image_raw/compressed");
    declare_parameter<std::string>("depth_topic", "bar30/depth");
    declare_parameter<std::string>("sonar_topic", "imagenex831l/sonar_health");
    declare_parameter<std::string>("imu_topic", "imu/data");
    declare_parameter<std::string>("tag_topic", "/aruco_markers");
    declare_parameter<std::string>("bag_topic", "/bag");

    std::string cam_topic;
    std::string depth_topic;
    std::string sonar_topic;
    std::string imu_topic;
    std::string tag_topic;
    std::string bag_topic;

    get_parameter("cam_topic", cam_topic);
    get_parameter("depth_topic", depth_topic);
    get_parameter("sonar_topic", sonar_topic);
    get_parameter("imu_topic", imu_topic);
    get_parameter("tag_topic", tag_topic);
    get_parameter("bag_topic", bag_topic);

    cam_sub_ = create_subscription<sensor_msgs::msg::CompressedImage>(
        cam_topic, 1, std::bind(&Ros2Node::cam_callback, this, std::placeholders::_1));

    depth_sub_ = create_subscription<std_msgs::msg::Float32>(
        depth_topic, 10, std::bind(&Ros2Node::depth_callback, this, std::placeholders::_1));

    sonar_sub_ = create_subscription<std_msgs::msg::String>(
        sonar_topic, 10, std::bind(&Ros2Node::sonar_callback, this, std::placeholders::_1));

    bag_sub_ = create_subscription<std_msgs::msg::String>(
        bag_topic, 10, std::bind(&Ros2Node::bag_callback, this, std::placeholders::_1));

    orin_sub_ = create_subscription<std_msgs::msg::String>(
        "orin", 10, std::bind(&Ros2Node::orin_callback, this, std::placeholders::_1));
    
    imu_sub_ = create_subscription<sensor_msgs::msg::Imu>(
        imu_topic, 10, std::bind(&Ros2Node::imu_callback, this, std::placeholders::_1));

    tag_sub_ = create_subscription<ros2_aruco_interfaces::msg::ArucoMarkers>(
        tag_topic, 1, std::bind(&Ros2Node::tag_callback, this, std::placeholders::_1));

    tag_id_pub_ = create_publisher<std_msgs::msg::Int32>("tag_id", 10);
}

Ros2Node::~Ros2Node()
{

    cam_sub_.reset();
    depth_sub_.reset();
    sonar_sub_.reset();
    imu_sub_.reset();
    orin_sub_.reset();
    tag_sub_.reset();
    tag_id_pub_.reset();
}

cv::Mat Ros2Node::getRosMsg() {
    return cv_ptr;
}

std::string Ros2Node::getDepth() {
    return (depth_sub_->get_publisher_count() > 0) ? std::to_string(depth) : "Not Active";
}

std::string Ros2Node::getSonar() {
    return (sonar_sub_->get_publisher_count() > 0) ? sonar : "Not Active";
}

std::string Ros2Node::getIMU() {
    return (imu_sub_->get_publisher_count() > 0) ? imu : "Not Active";
}

std::string Ros2Node::getOrin() {
    return orin;
}

std::string Ros2Node::getBag() {
    return bag;
}

void Ros2Node::cam_callback(const sensor_msgs::msg::CompressedImage::SharedPtr msg) {

    cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8)->image;
}

void Ros2Node::depth_callback(const std_msgs::msg::Float32::SharedPtr msg) {
    depth = msg->data;
}

void Ros2Node::sonar_callback(const std_msgs::msg::String::SharedPtr msg) {
    sonar = msg->data;
}

void Ros2Node::orin_callback(const std_msgs::msg::String::SharedPtr msg) {
    orin = msg->data;
}

void Ros2Node::bag_callback(const std_msgs::msg::String::SharedPtr msg) {
    bag = msg->data;
}

void Ros2Node::imu_callback(const sensor_msgs::msg::Imu::SharedPtr msg) {
    imu = (msg != nullptr) ? "Active" : "Not Active";
}

void Ros2Node::tag_callback(const ros2_aruco_interfaces::msg::ArucoMarkers::SharedPtr msg) {
    if (msg->marker_ids.empty()) {
        RCLCPP_INFO(this->get_logger(), "No tags detected.");
        return;
    }

    for (size_t i = 0; i < msg->marker_ids.size(); ++i) {
        auto tag_id_msg = std_msgs::msg::Int32();
        tag_id_msg.data = msg->marker_ids[i];
        tag_id_pub_->publish(tag_id_msg);

    }
}
