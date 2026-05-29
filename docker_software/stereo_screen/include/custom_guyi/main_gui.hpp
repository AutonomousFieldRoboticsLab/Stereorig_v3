#pragma once

#include <QMainWindow>
#include <QWidget>
#include <QPushButton>
#include <QLabel>
#include <QVBoxLayout>
#include <QImage>
#include <QTimer>
#include <QPixmap>
#include <QPainter>
#include <opencv2/opencv.hpp>
#include "custom_guyi/ros2node.hpp"

class MainGUI : public QMainWindow
{
    Q_OBJECT
public:
    explicit MainGUI(const std::shared_ptr<Ros2Node>&  ros2_node, QWidget* parent = nullptr);
    ~MainGUI() override;
    QPixmap showImage();
    void updateImage();
    QSize windowSize;
    int windowWidth;
    int windowHeight;
    bool once;
    std::string orin;
    int count;
    
private:
    const std::shared_ptr<Ros2Node> ros2_node;
    QLabel* imageFrame;
    QWidget* main_widget;
    QTimer* timer;
};