#include "MainWindow.h"
#include "ui_MainWindow.h"
#include <QVBoxLayout>
#include <QDateTime>
#include <QApplication>
#include <QStyleFactory>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    setWindowState(Qt::WindowMaximized);

    setupUI();
    createStatusBar();
    connectSignals();

    // 启动系统时间更新定时器
    systemTimer = new QTimer(this);
    connect(systemTimer, &QTimer::timeout, this, &MainWindow::onUpdateSystemTime);
    systemTimer->start(1000);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::setupUI()
{
    loadStyleSheet();

    // 设置左侧导航树的点击事件
    connect(ui->leftNavTree, &QTreeWidget::itemClicked, this, [this](QTreeWidgetItem *item) {
        int index = ui->leftNavTree->indexOfTopLevelItem(item);
        if (index >= 0) {
            ui->contentStack->setCurrentIndex(index);
        }
    });

    // 设置默认选中第4个页面（三维风场可视化）
    ui->leftNavTree->setCurrentItem(ui->leftNavTree->topLevelItem(3));
    ui->contentStack->setCurrentIndex(3);
}

void MainWindow::loadStyleSheet()
{
    QString styleSheet =
        "QMainWindow { background-color: #1e1e1e; }"
        "QMenuBar { background-color: #2d2d2d; color: #e0e0e0; border-bottom: 1px solid #3d3d3d; padding: 2px 4px; }"
        "QMenuBar::item:selected { background-color: #0078d4; color: white; border-radius: 3px; }"
        "QMenuBar::item:pressed { background-color: #005a9e; }"
        "QMenu { background-color: #2d2d2d; color: #e0e0e0; border: 1px solid #3d3d3d; }"
        "QMenu::item:selected { background-color: #0078d4; color: white; padding-left: 16px; }"
        "QMenu::separator { height: 1px; background: #3d3d3d; margin: 4px 0; }"
        "QTreeWidget { background-color: #252525; color: #e0e0e0; border-right: 2px solid #0078d4; outline: none; font-size: 11px; }"
        "QTreeWidget::item { padding: 6px 4px; border-radius: 3px; }"
        "QTreeWidget::item:selected { background-color: #0078d4; color: white; font-weight: bold; }"
        "QTreeWidget::item:hover { background-color: #404040; }"
        "QPushButton { background-color: #0078d4; color: white; border: none; border-radius: 4px; padding: 6px 16px; font-weight: bold; font-size: 11px; }"
        "QPushButton:hover { background-color: #1084e0; }"
        "QPushButton:pressed { background-color: #005a9e; }"
        "QPushButton:disabled { background-color: #404040; color: #808080; }"
        "QLabel { color: #e0e0e0; }"
        "QSplitter::handle { background-color: #3d3d3d; width: 2px; }"
        "QSplitter::handle:hover { background-color: #0078d4; }"
        "QScrollBar:vertical { background-color: #2a2a2a; width: 12px; }"
        "QScrollBar::handle:vertical { background-color: #555555; border-radius: 6px; min-height: 20px; }"
        "QScrollBar::handle:vertical:hover { background-color: #0078d4; }"
        "QScrollBar:horizontal { background-color: #2a2a2a; height: 12px; }"
        "QScrollBar::handle:horizontal { background-color: #555555; border-radius: 6px; min-width: 20px; }"
        "QScrollBar::handle:horizontal:hover { background-color: #0078d4; }";

    qApp->setStyle(QStyleFactory::create("Fusion"));
    qApp->setStyleSheet(styleSheet);
}

void MainWindow::createStatusBar()
{
    // 系统状态指示器
    systemStatusIndicator = new StatusIndicator();
    systemStatusIndicator->setStatus(StatusIndicator::Green);
    systemStatusIndicator->setText(tr("系统正常"));
    systemStatusIndicator->setToolTip(tr("系统状态：运行中"));

    // 创建状态栏的各个标签
    QLabel *scanModeLabel = new QLabel(tr("扫描模式: PPI"));
    scanModeLabel->setStyleSheet("color: #e0e0e0; padding: 2px 6px;");

    QLabel *deviceStatusLabel = new QLabel(tr("设备状态: 已连接"));
    deviceStatusLabel->setStyleSheet("color: #e0e0e0; padding: 2px 6px;");

    QLabel *dataCollectionLabel = new QLabel(tr("采集状态: 待机"));
    dataCollectionLabel->setStyleSheet("color: #e0e0e0; padding: 2px 6px;");

    QLabel *systemTimeLabel = new QLabel(QDateTime::currentDateTime().toString("yyyy-MM-dd hh:mm:ss"));
    systemTimeLabel->setStyleSheet("color: #0078d4; padding: 2px 6px; font-weight: bold;");
    systemTimeLabel->setObjectName("systemTimeLabel");

    QLabel *runtimeLabel = new QLabel(tr("运行时长: 0h 0m 0s"));
    runtimeLabel->setStyleSheet("color: #e0e0e0; padding: 2px 6px;");

    // 添加到状态栏
    ui->statusbar->addWidget(systemStatusIndicator);
    ui->statusbar->addWidget(scanModeLabel);
    ui->statusbar->addWidget(deviceStatusLabel);
    ui->statusbar->addWidget(dataCollectionLabel);

    // 添加弹性空间
    QWidget *spacer = new QWidget();
    spacer->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    ui->statusbar->addWidget(spacer);

    ui->statusbar->addWidget(systemTimeLabel);
    ui->statusbar->addWidget(runtimeLabel);
}

void MainWindow::connectSignals()
{
    // 连接菜单动作
    connect(ui->actionExit, &QAction::triggered, this, &QApplication::quit);
    connect(ui->actionFullScreen, &QAction::triggered, this, [this]() {
        if (windowState() & Qt::WindowFullScreen) {
            showNormal();
        } else {
            showFullScreen();
        }
    });
}

void MainWindow::onUpdateSystemTime()
{
    QLabel *timeLabel = findChild<QLabel *>("systemTimeLabel");
    if (timeLabel) {
        timeLabel->setText(QDateTime::currentDateTime().toString("yyyy-MM-dd hh:mm:ss"));
    }
}

void MainWindow::onNavItemClicked(int index)
{
    ui->contentStack->setCurrentIndex(index);
}
