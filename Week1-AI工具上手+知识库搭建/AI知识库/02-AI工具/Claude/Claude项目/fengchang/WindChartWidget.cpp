#include "WindChartWidget.h"
#include <QPainter>
#include <QPen>
#include <QBrush>
#include <QFont>
#include <cmath>

WindChartWidget::WindChartWidget(ChartType type, QWidget *parent)
    : QWidget(parent), chartType(type)
{
    setMinimumHeight(100);
    setStyleSheet("background-color: white;");
}

WindChartWidget::~WindChartWidget()
{
}

void WindChartWidget::updateData(const QVector<float> &values, const QVector<qint64> &timestamps)
{
    dataValues = values;
    this->timestamps = timestamps;

    // 检查是否有数据触及告警阈值
    isAlarm = false;
    for (float value : dataValues) {
        if (std::abs(value) >= thresholdValue) {
            isAlarm = true;
            alarmFlashCounter = 0;
            break;
        }
    }

    update();
}

void WindChartWidget::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing, true);

    // 绘制背景
    painter.fillRect(rect(), Qt::white);

    switch (chartType) {
        case Longitudinal:
            drawLongitudinalChart(painter);
            break;
        case Lateral:
            drawLateralChart(painter);
            break;
        case Vertical:
            drawVerticalChart(painter);
            break;
    }

    drawZeroLine(painter);
    drawThresholdLines(painter);
    drawLegend(painter);
}

void WindChartWidget::resizeEvent(QResizeEvent *event)
{
    QWidget::resizeEvent(event);
}

void WindChartWidget::drawLongitudinalChart(QPainter &painter)
{
    int w = width();
    int h = height();
    int margin = 40;

    // 绘制坐标轴
    QPen axisPen(Qt::black, 1);
    painter.setPen(axisPen);

    // Y 轴
    painter.drawLine(margin, margin, margin, h - margin);
    // X 轴
    painter.drawLine(margin, h - margin, w - margin, h - margin);

    int graphWidth = w - 2 * margin;
    int graphHeight = h - 2 * margin;

    if (dataValues.isEmpty()) {
        return;
    }

    // 绘制曲线
    QPen curvePen(Qt::blue, 2);
    painter.setPen(curvePen);

    float range = maxValue - minValue;
    int dataSize = dataValues.size();

    for (int i = 1; i < dataSize; ++i) {
        float y1 = (dataValues[i - 1] - minValue) / range;
        float y2 = (dataValues[i] - minValue) / range;

        int x1 = margin + (i - 1) * graphWidth / dataSize;
        int x2 = margin + i * graphWidth / dataSize;
        int py1 = h - margin - y1 * graphHeight;
        int py2 = h - margin - y2 * graphHeight;

        // 根据数据值选择颜色（冷暖色表示）
        if (dataValues[i - 1] >= 0) {
            painter.setPen(QPen(QColor(255, 100, 100), 2));  // 红色（顺风）
        } else {
            painter.setPen(QPen(QColor(100, 150, 255), 2));  // 蓝色（逆风）
        }

        painter.drawLine(x1, py1, x2, py2);
    }

    // 绘制坐标标签
    QFont font = painter.font();
    font.setPointSize(8);
    painter.setFont(font);

    // Y 轴标签
    painter.setPen(Qt::black);
    for (int i = -2; i <= 2; ++i) {
        float value = minValue + (i + 2) * (maxValue - minValue) / 4;
        int y = h - margin - (i + 2) * graphHeight / 4;
        painter.drawText(margin - 35, y - 5, 30, 10, Qt::AlignRight, QString::number(value, 'f', 1));
    }

    // X 轴标签
    painter.drawText(w / 2 - 20, h - 5, 40, 20, Qt::AlignCenter, "时间 (s)");
}

void WindChartWidget::drawLateralChart(QPainter &painter)
{
    int w = width();
    int h = height();
    int margin = 40;

    // 绘制坐标轴
    QPen axisPen(Qt::black, 1);
    painter.setPen(axisPen);

    painter.drawLine(margin, margin, margin, h - margin);
    painter.drawLine(margin, h - margin, w - margin, h - margin);

    int graphWidth = w - 2 * margin;
    int graphHeight = h - 2 * margin;

    if (dataValues.isEmpty()) {
        return;
    }

    // 绘制箭头表示左右侧风
    float range = maxValue - minValue;
    float avgValue = 0;
    for (float v : dataValues) {
        avgValue += v;
    }
    avgValue /= dataValues.size();

    int centerY = h - margin;
    int arrowX = margin + graphWidth / 2;

    // 绘制箭头
    QPen arrowPen(Qt::darkGreen, 3);
    painter.setPen(arrowPen);

    if (avgValue > 0) {
        // 向上箭头（右侧风）
        painter.drawLine(arrowX, centerY, arrowX, centerY - 30);
        painter.drawLine(arrowX, centerY - 30, arrowX - 5, centerY - 25);
        painter.drawLine(arrowX, centerY - 30, arrowX + 5, centerY - 25);
    } else if (avgValue < 0) {
        // 向下箭头（左侧风）
        painter.drawLine(arrowX, centerY, arrowX, centerY + 30);
        painter.drawLine(arrowX, centerY + 30, arrowX - 5, centerY + 25);
        painter.drawLine(arrowX, centerY + 30, arrowX + 5, centerY + 25);
    }

    // 绘制坐标标签
    QFont font = painter.font();
    font.setPointSize(8);
    painter.setFont(font);
    painter.setPen(Qt::black);
    painter.drawText(margin - 30, h - margin + 10, 25, 15, Qt::AlignCenter, "测风");
}

void WindChartWidget::drawVerticalChart(QPainter &painter)
{
    int w = width();
    int h = height();
    int margin = 40;

    // 绘制坐标轴
    QPen axisPen(Qt::black, 1);
    painter.setPen(axisPen);

    painter.drawLine(margin, margin, margin, h - margin);
    painter.drawLine(margin, h - margin, w - margin, h - margin);

    int graphWidth = w - 2 * margin;
    int graphHeight = h - 2 * margin;
    int centerY = h - margin;

    if (dataValues.isEmpty()) {
        return;
    }

    // 绘制柱形图
    float range = maxValue - minValue;
    int dataSize = dataValues.size();
    int barWidth = graphWidth / (dataSize + 1);

    for (int i = 0; i < dataSize; ++i) {
        float normalizedValue = (dataValues[i] - minValue) / range;
        int barHeight = normalizedValue * graphHeight;

        int barX = margin + (i + 1) * barWidth;

        // 上升气流用暖色，下沉气流用冷色
        if (dataValues[i] >= 0) {
            painter.fillRect(barX - barWidth / 2 + 2, centerY - barHeight, barWidth - 4, barHeight,
                           QColor(255, 100, 100));  // 红色（上升）
        } else {
            painter.fillRect(barX - barWidth / 2 + 2, centerY, barWidth - 4, -barHeight,
                           QColor(100, 150, 255));  // 蓝色（下沉）
        }
    }

    // 绘制坐标标签
    QFont font = painter.font();
    font.setPointSize(8);
    painter.setFont(font);
    painter.setPen(Qt::black);
    painter.drawText(margin - 35, h - margin - 10, 30, 20, Qt::AlignCenter, "上升");
    painter.drawText(margin - 35, h - margin + 5, 30, 20, Qt::AlignCenter, "下沉");
}

void WindChartWidget::drawZeroLine(QPainter &painter)
{
    int w = width();
    int h = height();
    int margin = 40;
    int centerY = h - margin;

    // 绘制亮白色零线（虚线）
    QPen zeroPen(Qt::white, 2);
    zeroPen.setDashPattern({4, 4});
    painter.setPen(zeroPen);
    painter.drawLine(margin, centerY, w - margin, centerY);
}

void WindChartWidget::drawThresholdLines(QPainter &painter)
{
    int w = width();
    int h = height();
    int margin = 40;
    int graphHeight = h - 2 * margin;
    float range = maxValue - minValue;

    // 绘制安全阈值线（红色半透明虚线）
    QPen thresholdPen(Qt::red, 1);
    thresholdPen.setDashPattern({4, 4});
    painter.setPen(thresholdPen);

    // 上阈值线
    float normalizedThreshold = (thresholdValue - minValue) / range;
    int upperY = h - margin - normalizedThreshold * graphHeight;
    painter.drawLine(margin, upperY, w - margin, upperY);

    // 下阈值线
    normalizedThreshold = (-thresholdValue - minValue) / range;
    int lowerY = h - margin - normalizedThreshold * graphHeight;
    painter.drawLine(margin, lowerY, w - margin, lowerY);

    // 如果触发告警，闪烁显示
    if (isAlarm) {
        alarmFlashCounter++;
        if (alarmFlashCounter % 10 < 5) {
            painter.fillRect(rect(), QColor(255, 0, 0, 30));  // 半透明红色背景闪烁
        }
    }
}

void WindChartWidget::drawLegend(QPainter &painter)
{
    int margin = 10;
    QFont font = painter.font();
    font.setPointSize(9);
    font.setBold(true);
    painter.setFont(font);

    QString legendText;
    switch (chartType) {
        case Longitudinal:
            legendText = "顺/逆风 (Longitudinal)";
            break;
        case Lateral:
            legendText = "测风 (Lateral)";
            break;
        case Vertical:
            legendText = "垂直风 (Vertical)";
            break;
    }

    painter.setPen(Qt::black);
    painter.drawText(margin, margin, 200, 20, Qt::AlignLeft | Qt::AlignTop, legendText);
}
