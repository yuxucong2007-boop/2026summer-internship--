#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTimer>
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
    void createStatusBar();
    void connectSignals();

    Ui::MainWindow *ui;
    StatusIndicator *systemStatusIndicator;
    QTimer *systemTimer;
};

#endif // MAINWINDOW_H
