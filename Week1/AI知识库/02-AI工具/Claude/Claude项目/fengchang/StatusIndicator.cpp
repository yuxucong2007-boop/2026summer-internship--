#include "StatusIndicator.h"
#include <QPainter>
#include <QTimerEvent>

StatusIndicator::StatusIndicator(QWidget *parent)
    : QWidget(parent), currentColor(Green), isBlinking(false), timerId(-1), blinkState(true)
{
    setMinimumSize(80, 24);
    setMaximumSize(80, 24);
}

StatusIndicator::~StatusIndicator()
{
    if (timerId != -1) {
        killTimer(timerId);
    }
}

void StatusIndicator::setStatus(StatusColor color)
{
    currentColor = color;
    update();
}

void StatusIndicator::setText(const QString &text)
{
    statusText = text;
    update();
}

void StatusIndicator::setBlinking(bool blink)
{
    isBlinking = blink;
    if (blink && timerId == -1) {
        timerId = startTimer(500);
    } else if (!blink && timerId != -1) {
        killTimer(timerId);
        timerId = -1;
        blinkState = true;
    }
}

void StatusIndicator::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing, true);

    // 绘制背景
    painter.fillRect(rect(), QColor(30, 30, 30));

    // 绘制状态灯
    if (!isBlinking || blinkState) {
        QColor indicatorColor = getColorByStatus(currentColor);
        painter.setBrush(indicatorColor);
        painter.setPen(QColor(80, 80, 80));
        painter.drawEllipse(8, 6, 12, 12);

        // 发光效果
        painter.setBrush(Qt::NoBrush);
        painter.setPen(QPen(indicatorColor, 1));
        painter.setOpacity(0.5);
        painter.drawEllipse(6, 4, 16, 16);
    }

    // 绘制文本
    painter.setOpacity(1.0);
    painter.setPen(QColor(224, 224, 224));
    QFont font;
    font.setPointSize(8);
    painter.setFont(font);
    painter.drawText(26, 0, 50, 24, Qt::AlignLeft | Qt::AlignVCenter, statusText);
}

void StatusIndicator::timerEvent(QTimerEvent *event)
{
    if (event->timerId() == timerId) {
        blinkState = !blinkState;
        update();
    }
}

QColor StatusIndicator::getColorByStatus(StatusColor color) const
{
    switch (color) {
        case Green:
            return QColor(0, 200, 100);
        case Yellow:
            return QColor(255, 200, 0);
        case Red:
            return QColor(255, 80, 80);
        default:
            return QColor(128, 128, 128);
    }
}
