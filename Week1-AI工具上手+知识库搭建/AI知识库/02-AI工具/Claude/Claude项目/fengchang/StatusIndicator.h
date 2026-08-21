#ifndef STATUSINDICATOR_H
#define STATUSINDICATOR_H

#include <QWidget>
#include <QLabel>

class StatusIndicator : public QWidget
{
    Q_OBJECT

public:
    enum StatusColor {
        Green,   // 正常
        Yellow,  // 警告
        Red      // 错误
    };

    explicit StatusIndicator(QWidget *parent = nullptr);
    ~StatusIndicator();

    void setStatus(StatusColor color);
    void setText(const QString &text);
    void setBlinking(bool blink);

protected:
    void paintEvent(QPaintEvent *event) override;
    void timerEvent(QTimerEvent *event) override;

private:
    StatusColor currentColor;
    QString statusText;
    bool isBlinking;
    int timerId;
    bool blinkState;

    QColor getColorByStatus(StatusColor color) const;
};

#endif // STATUSINDICATOR_H
