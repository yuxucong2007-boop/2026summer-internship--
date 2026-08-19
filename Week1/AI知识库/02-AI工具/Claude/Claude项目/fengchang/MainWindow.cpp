#include "MainWindow.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QMenuBar>
#include <QMenu>
#include <QAction>
#include <QTreeWidgetItem>
#include <QHeaderView>
#include <QDateTime>
#include <QTimer>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle(tr("测风激光雷达控制系统 - 主界面"));
    setWindowState(Qt::WindowMaximized);

    setupUI();
    connectSignals();

    // 启动系统时间更新定时器
    QTimer *timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, [this]() {
        systemTimeLabel->setText(QDateTime::currentDateTime().toString("yyyy-MM-dd hh:mm:ss"));
    });
    timer->start(1000);
}

MainWindow::~MainWindow()
{
}

void MainWindow::setupUI()
{
    createMenuBar();
    createCentralWidget();
    createLeftNavigation();
    createStatusBar();
}

void MainWindow::createMenuBar()
{
    createSystemMenu();
    createDeviceMenu();
    createMeasurementMenu();
    createViewMenu();
    createDataMenu();
    createHelpMenu();
}

void MainWindow::createSystemMenu()
{
    QMenu *systemMenu = menuBar()->addMenu(tr("系统"));
    systemMenu->addAction(tr("登录/注销"));
    systemMenu->addAction(tr("用户管理"));
    systemMenu->addAction(tr("系统设置"));
    systemMenu->addSeparator();
    systemMenu->addAction(tr("退出"));
}

void MainWindow::createDeviceMenu()
{
    QMenu *deviceMenu = menuBar()->addMenu(tr("设备"));
    deviceMenu->addAction(tr("设备连接"));
    deviceMenu->addAction(tr("设备状态"));
    deviceMenu->addAction(tr("参数配置"));
    deviceMenu->addAction(tr("自检测"));
}

void MainWindow::createMeasurementMenu()
{
    QMenu *measurementMenu = menuBar()->addMenu(tr("测量"));
    measurementMenu->addAction(tr("扫描模式选择"));
    measurementMenu->addAction(tr("测量启动"));
    measurementMenu->addAction(tr("测量停止"));
    measurementMenu->addAction(tr("参数调整"));
}

void MainWindow::createViewMenu()
{
    QMenu *viewMenu = menuBar()->addMenu(tr("视图"));
    viewMenu->addAction(tr("工作区显示"));
    viewMenu->addAction(tr("全屏模式"));
    viewMenu->addAction(tr("重置布局"));
}

void MainWindow::createDataMenu()
{
    QMenu *dataMenu = menuBar()->addMenu(tr("数据"));
    dataMenu->addAction(tr("数据存储设置"));
    dataMenu->addAction(tr("数据导出"));
    dataMenu->addAction(tr("历史回放"));
}

void MainWindow::createHelpMenu()
{
    QMenu *helpMenu = menuBar()->addMenu(tr("帮助"));
    helpMenu->addAction(tr("用户手册"));
    helpMenu->addAction(tr("操作指南"));
    helpMenu->addSeparator();
    helpMenu->addAction(tr("关于"));
}

void MainWindow::createCentralWidget()
{
    centralWidget = new QWidget;
    setCentralWidget(centralWidget);

    // 创建主分割器
    mainSplitter = new QSplitter(Qt::Horizontal);

    // ========== 左侧导航面板 ==========
    leftNavTree = new QTreeWidget;
    leftNavTree->setColumnCount(1);
    leftNavTree->header()->hide();
    leftNavTree->setMaximumWidth(180);
    leftNavTree->setMinimumWidth(120);

    // ========== 中间内容区域 ==========
    contentStack = new QStackedWidget;

    // 创建 3D 可视化页面（主界面）
    QWidget *mainVisualizationPage = new QWidget;

    // 主 3D 视口（占比 70%）
    visualization3D = new QOpenGLWidget;
    visualization3D->setMinimumSize(800, 600);
    visualization3D->setStyleSheet(
        "QOpenGLWidget {"
        "  border: 2px solid #0078d4;"
        "  border-radius: 4px;"
        "  background-color: #0a0a0a;"
        "}"
    );

    // 右侧风矢量面板（占比 30%）
    windVisualizationPanel = new QWidget;
    windVisualizationPanel->setMaximumWidth(320);
    windVisualizationPanel->setMinimumWidth(280);
    windVisualizationPanel->setStyleSheet(
        "QWidget {"
        "  background-color: #252525;"
        "  border-left: 2px solid #0078d4;"
        "}"
    );

    QVBoxLayout *windPanelLayout = new QVBoxLayout(windVisualizationPanel);
    windPanelLayout->setContentsMargins(12, 12, 12, 12);
    windPanelLayout->setSpacing(8);

    // 风矢量图表标题
    QLabel *windTitle = new QLabel(tr("风矢量可视化"));
    windTitle->setStyleSheet(
        "QLabel {"
        "  font-weight: bold;"
        "  font-size: 13px;"
        "  color: #0078d4;"
        "  padding: 4px 0;"
        "}"
    );
    windPanelLayout->addWidget(windTitle);

    // 三个风场图表容器
    windChart1 = new QWidget;
    windChart1->setStyleSheet(
        "QWidget {"
        "  background-color: #1a1a1a;"
        "  border: 1px solid #404040;"
        "  border-radius: 4px;"
        "}"
    );
    windChart1->setMinimumHeight(90);
    windPanelLayout->addWidget(windChart1);

    QLabel *chart1Label = new QLabel(tr("顺/逆风 (Longitudinal)"));
    chart1Label->setStyleSheet("font-size: 9px; color: #0078d4; padding: 2px 4px;");
    windPanelLayout->addWidget(chart1Label);

    windChart2 = new QWidget;
    windChart2->setStyleSheet(
        "QWidget {"
        "  background-color: #1a1a1a;"
        "  border: 1px solid #404040;"
        "  border-radius: 4px;"
        "}"
    );
    windChart2->setMinimumHeight(90);
    windPanelLayout->addWidget(windChart2);

    QLabel *chart2Label = new QLabel(tr("测风 (Lateral)"));
    chart2Label->setStyleSheet("font-size: 9px; color: #0078d4; padding: 2px 4px;");
    windPanelLayout->addWidget(chart2Label);

    windChart3 = new QWidget;
    windChart3->setStyleSheet(
        "QWidget {"
        "  background-color: #1a1a1a;"
        "  border: 1px solid #404040;"
        "  border-radius: 4px;"
        "}"
    );
    windChart3->setMinimumHeight(90);
    windPanelLayout->addWidget(windChart3);

    QLabel *chart3Label = new QLabel(tr("垂直风 (Vertical)"));
    chart3Label->setStyleSheet("font-size: 9px; color: #0078d4; padding: 2px 4px;");
    windPanelLayout->addWidget(chart3Label);

    windPanelLayout->addStretch();

    // 主 3D 视口左下角和右下角的切片视图
    QWidget *bottomViewsContainer = new QWidget;
    QHBoxLayout *bottomViewsLayout = new QHBoxLayout(bottomViewsContainer);
    bottomViewsLayout->setContentsMargins(0, 0, 0, 0);

    sliceViewHorizontal = new QWidget;
    sliceViewHorizontal->setStyleSheet(
        "QWidget {"
        "  background-color: #0a0a0a;"
        "  border: 1px solid #0078d4;"
        "  border-radius: 3px;"
        "}"
    );
    sliceViewHorizontal->setMinimumSize(140, 140);
    QLabel *sliceLabel1 = new QLabel(tr("水平切片\n(俯视)"));
    sliceLabel1->setStyleSheet("color: #0078d4; text-align: center; font-size: 10px; font-weight: bold;");
    sliceLabel1->setAlignment(Qt::AlignCenter);
    QVBoxLayout *sliceLayout1 = new QVBoxLayout(sliceViewHorizontal);
    sliceLayout1->setContentsMargins(4, 4, 4, 4);
    sliceLayout1->addWidget(sliceLabel1);

    sliceViewVertical = new QWidget;
    sliceViewVertical->setStyleSheet(
        "QWidget {"
        "  background-color: #0a0a0a;"
        "  border: 1px solid #0078d4;"
        "  border-radius: 3px;"
        "}"
    );
    sliceViewVertical->setMinimumSize(140, 140);
    QLabel *sliceLabel2 = new QLabel(tr("垂直切片\n(剖面)"));
    sliceLabel2->setStyleSheet("color: #0078d4; text-align: center; font-size: 10px; font-weight: bold;");
    sliceLabel2->setAlignment(Qt::AlignCenter);
    QVBoxLayout *sliceLayout2 = new QVBoxLayout(sliceViewVertical);
    sliceLayout2->setContentsMargins(4, 4, 4, 4);
    sliceLayout2->addWidget(sliceLabel2);

    bottomViewsLayout->addWidget(sliceViewHorizontal);
    bottomViewsLayout->addWidget(sliceViewVertical);
    bottomViewsLayout->addStretch();

    // 主 3D 视口布局（嵌入左下和右下切片视图）
    QWidget *visualizationWrapper = new QWidget;
    QVBoxLayout *visWrapperLayout = new QVBoxLayout(visualizationWrapper);
    visWrapperLayout->setContentsMargins(0, 0, 0, 0);

    visWrapperLayout->addWidget(visualization3D);
    visWrapperLayout->addWidget(bottomViewsContainer, 0, Qt::AlignBottom);

    // 画中画窗口（右上角悬浮）
    pictureinPicture = new QLabel;
    pictureinPicture->setStyleSheet("background-color: #1a1a1a; border: 2px solid #444;");
    pictureinPicture->setMinimumSize(150, 120);
    pictureinPicture->setText(tr("光窗监控\n(UVC 视频流)"));
    pictureinPicture->setAlignment(Qt::AlignCenter);
    pictureinPicture->setStyleSheet(
        "background-color: #1a1a1a; "
        "border: 2px solid #444; "
        "color: white; "
        "font-size: 10px;"
    );

    // 主界面总体布局（3D + 右侧风矢量面板）
    QHBoxLayout *mainVisHLayout = new QHBoxLayout;
    mainVisHLayout->setContentsMargins(0, 0, 0, 0);
    mainVisHLayout->addWidget(visualizationWrapper, 1);
    mainVisHLayout->addWidget(windVisualizationPanel);

    mainVisualizationPage->setLayout(mainVisHLayout);
    contentStack->addWidget(mainVisualizationPage);

    // ========== 其他 7 个功能页面（占位符）==========
    for (int i = 1; i < 8; ++i) {
        QWidget *placeholderPage = new QWidget;
        QVBoxLayout *layout = new QVBoxLayout(placeholderPage);
        QLabel *label = new QLabel(tr("功能页面 %1").arg(i + 1));
        label->setStyleSheet("font-size: 16px; font-weight: bold;");
        layout->addWidget(label);
        layout->addStretch();
        contentStack->addWidget(placeholderPage);
    }

    // ========== 组装主分割器 ==========
    mainSplitter->addWidget(leftNavTree);
    mainSplitter->addWidget(contentStack);
    mainSplitter->setStretchFactor(0, 0);
    mainSplitter->setStretchFactor(1, 1);

    // ========== 设置中央窗口 ==========
    QVBoxLayout *centralLayout = new QVBoxLayout(centralWidget);
    centralLayout->setContentsMargins(0, 0, 0, 0);
    centralLayout->addWidget(mainSplitter);

    centralWidget->setLayout(centralLayout);
}

void MainWindow::createLeftNavigation()
{
    QStringList navItems = {
        tr("系统总览（仪表盘）"),
        tr("设备控制与状态监测"),
        tr("风场数据采集"),
        tr("三维风场可视化"),
        tr("二维风场可视化"),
        tr("危害风场识别告警"),
        tr("数据管理与回放"),
        tr("系统维护与日志")
    };

    for (int i = 0; i < navItems.size(); ++i) {
        QTreeWidgetItem *item = new QTreeWidgetItem(leftNavTree);
        item->setText(0, navItems[i]);
        item->setData(0, Qt::UserRole, i);

        // 设置样式
        if (i == 3) {  // 默认选中"三维风场可视化"
            item->setSelected(true);
            leftNavTree->setCurrentItem(item);
        }
    }

    // 连接导航树的选择信号
    connect(leftNavTree, &QTreeWidget::itemClicked, this, [this](QTreeWidgetItem *item) {
        int index = item->data(0, Qt::UserRole).toInt();
        contentStack->setCurrentIndex(index);
    });
}

void MainWindow::createStatusBar()
{
    // 系统状态指示灯
    systemStatusLight = new QLabel;
    systemStatusLight->setStyleSheet(
        "border-radius: 6px; "
        "background-color: #00aa00; "
        "width: 12px; height: 12px; "
        "margin: 0px 5px;"
    );
    systemStatusLight->setToolTip(tr("系统状态：运行中（绿=正常、黄=警告、红=错误）"));

    // 扫描模式
    scanModeLabel = new QLabel(tr("扫描模式: PPI"));

    // 设备连接状态
    deviceStatusLabel = new QLabel(tr("设备状态: 已连接"));

    // 数据采集状态
    dataCollectionLabel = new QLabel(tr("采集状态: 待机"));

    // 系统时间
    systemTimeLabel = new QLabel(QDateTime::currentDateTime().toString("yyyy-MM-dd hh:mm:ss"));

    // 累计运行时长
    runtimeLabel = new QLabel(tr("运行时长: 0h 0m 0s"));

    // 添加到状态栏
    statusBar()->addWidget(systemStatusLight);
    statusBar()->addWidget(scanModeLabel);
    statusBar()->addWidget(deviceStatusLabel);
    statusBar()->addWidget(dataCollectionLabel);

    // 添加弹性空间
    QWidget *spacer = new QWidget();
    spacer->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    statusBar()->addWidget(spacer);

    statusBar()->addWidget(systemTimeLabel);
    statusBar()->addWidget(runtimeLabel);

    // 设置状态栏样式
    statusBar()->setStyleSheet(
        "QStatusBar {"
        "  background-color: #2d2d2d;"
        "  color: #e0e0e0;"
        "  border-top: 2px solid #0078d4;"
        "  padding: 2px 0;"
        "}"
    );
}

void MainWindow::connectSignals()
{
    // 后续可添加各种信号槽连接
}
