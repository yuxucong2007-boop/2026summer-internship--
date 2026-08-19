#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QWidget>
#include <QSplitter>
#include <QTreeWidget>
#include <QStackedWidget>
#include <QLabel>
#include <QStatusBar>
#include <QOpenGLWidget>
#include <QApplication>
#include <QStyleFactory>
#include <QTimer>
#include <QAction>
#include "StatusIndicator.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void onUpdateSystemTime();
    void onNavItemClicked(int index);

private:
    void setupUI();
    void loadStyleSheet();
    void createMenuBar();
    void createLeftNavigation();
    void createCentralWidget();
    void createStatusBar();
    void connectSignals();

    // 菜单栏相关
    void createSystemMenu();
    void createDeviceMenu();
    void createMeasurementMenu();
    void createViewMenu();
    void createDataMenu();
    void createHelpMenu();

    // UI 对象
    Ui::MainWindow *ui;

    // 状态栏组件
    StatusIndicator *systemStatusIndicator;  // 系统状态指示器
    QTimer *systemTimer;                     // 系统时间定时器
};

#endif // MAINWINDOW_H
