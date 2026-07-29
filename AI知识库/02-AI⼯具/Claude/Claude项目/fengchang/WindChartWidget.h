#ifndef WINDCHARTWIDGET_H
#define WINDCHARTWIDGET_H

#include <QWidget>
#include <QVector>

class WindChartWidget : public QWidget
{
    Q_OBJECT

public:
    enum ChartType {
        Longitudinal,  // 顺/逆风
        Lateral,       // 测风（横向）
        Vertical       // 垂直风
    };

    explicit WindChartWidget(ChartType type, QWidget *parent = nullptr);
    ~WindChartWidget();

    void setChartType(ChartType type) { chartType = type; }
    void updateData(const QVector<float> &values, const QVector<qint64> &timestamps);

protected:
    void paintEvent(QPaintEvent *event) override;
    void resizeEvent(QResizeEvent *event) override;

private:
    void drawLongitudinalChart(QPainter &painter);
    void drawLateralChart(QPainter &painter);
    void drawVerticalChart(QPainter &painter);
    void drawZeroLine(QPainter &painter);
    void drawThresholdLines(QPainter &painter);
    void drawLegend(QPainter &painter);

    ChartType chartType;
    QVector<float> dataValues;        // 风速数据
    QVector<qint64> timestamps;        // 时间戳
    float maxValue = 20.0f;           // Y 轴最大值 (m/s)
    float minValue = -20.0f;          // Y 轴最小值 (m/s)
    float thresholdValue = 10.0f;     // 安全阈值
    bool isAlarm = false;             // 是否告警
    int alarmFlashCounter = 0;        // 告警闪烁计数器
};

#endif // WINDCHARTWIDGET_H
