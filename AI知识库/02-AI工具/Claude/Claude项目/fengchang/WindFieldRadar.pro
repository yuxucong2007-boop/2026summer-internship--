QT += core gui opengl

CONFIG += c++11

TARGET = WindFieldRadar
TEMPLATE = app

SOURCES += \
    main.cpp \
    MainWindow_ui.cpp \
    WindChartWidget.cpp \
    StatusIndicator.cpp

HEADERS += \
    MainWindow.h \
    WindChartWidget.h \
    StatusIndicator.h

FORMS += \
    MainWindow.ui

# Default rules for deployment
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
