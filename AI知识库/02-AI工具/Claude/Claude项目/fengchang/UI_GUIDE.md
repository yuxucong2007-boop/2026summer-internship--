# Qt UI 文件使用指南

## 📋 文件说明

本项目现已支持 Qt Designer 生成的 UI 文件，文件结构如下：

### 核心文件
- **MainWindow.ui** - Qt Designer 界面设计文件（可用 Qt Designer 编辑）
- **MainWindow_ui.h** - UI 文件定义头
- **MainWindow_ui.cpp** - UI 文件实现
- **MainWindow.h** - 主窗口类头文件
- **StatusIndicator.h/cpp** - 状态指示器组件
- **WindChartWidget.h/cpp** - 风矢量图表组件
- **main.cpp** - 程序入口

## 🔧 在 Qt Creator 中编译和运行

### 方法一：打开 .pro 项目文件（推荐）

1. **打开 Qt Creator**
2. **点击菜单** → `文件` → `打开文件或工程`
3. **选择** `D:/Claude/fengchang/WindFieldRadar.pro`
4. **选择编译工具链**
   - 如果弹出配置对话框，选择 `Desktop Qt 5.14.2 MinGW 32-bit`
   - 点击 `下一步` → `完成`
5. **编译项目**
   - 按 `Ctrl+B` 或点击 `构建` → `构建全部`
   - 等待编译完成（首次编译可能较慢）
6. **运行程序**
   - 按 `Ctrl+R` 或点击 `构建` → `运行`

### 方法二：在 Qt Designer 中编辑 UI 文件

1. **打开 Qt Creator**
2. **点击菜单** → `文件` → `打开文件`
3. **选择** `D:/Claude/fengchang/MainWindow.ui`
4. **进入 Qt Designer 编辑模式**
5. **修改界面设计**（拖拽组件、修改属性等）
6. **保存修改** （Ctrl+S）

> **注意**：修改 .ui 文件后，编译时会自动生成新的 `ui_MainWindow.h` 文件

## 🎨 界面组件说明

### 菜单栏 (QMenuBar)
```
系统
├── 登录/注销
├── 用户管理
├── 系统设置
└── 退出

设备
├── 设备连接
├── 设备状态
├── 参数配置
└── 自检测

测量
├── 扫描模式选择
├── 测量启动
├── 测量停止
└── 参数调整

视图
├── 工作区显示
├── 全屏模式
└── 重置布局

数据
├── 数据存储设置
├── 数据导出
└── 历史回放

帮助
├── 用户手册
├── 操作指南
└── 关于
```

### 左侧导航树 (QTreeWidget)
- 系统总览（仪表盘）
- 设备控制与状态监测
- 风场数据采集
- 三维风场可视化（默认选中）
- 二维风场可视化
- 危害风场识别告警
- 数据管理与回放
- 系统维护与日志

### 中央内容区 (QStackedWidget)
- 包含 8 个页面（对应左侧导航树的 8 个项目）
- 点击左侧导航树自动切换页面

### 主界面布局（第4页：三维风场可视化）

```
┌─────────────────────────────────────────┐
│       3D 风场可视化区域                  │  风矢量
│       (QOpenGLWidget)                   │  图表区
│       1000x600 最小尺寸                 │  (280-320px)
│       ┌────────────┬────────────┐       │
│       │ 水平切片   │ 垂直切片   │       │
│       │ 140x140    │ 140x140    │       │
│       └────────────┴────────────┘       │
└─────────────────────────────────────────┘
```

### 风矢量图表面板
- **顺/逆风图表** (Longitudinal) - 90px 高
- **测风图表** (Lateral) - 90px 高  
- **垂直风图表** (Vertical) - 90px 高

### 状态栏 (QStatusBar)
- 系统状态指示灯（绿/黄/红）
- 扫描模式标签
- 设备连接状态标签
- 数据采集状态标签
- 弹性空间
- 系统时间（实时更新）
- 累计运行时长

## 🎯 修改界面的步骤

### 添加新的菜单项
1. 在 Qt Designer 中打开 `MainWindow.ui`
2. 双击菜单栏中的菜单
3. 输入新菜单项的名称
4. 右键点击新菜单项 → `改变对象名...` 设置对象名
5. 保存文件

### 修改菜单样式
1. 在 Qt Designer 中选中菜单栏
2. 在属性面板中找到 `styleSheet` 属性
3. 修改样式字符串
4. 保存文件

### 添加新的导航页面
1. 在 Qt Designer 中选中 `contentStack` (QStackedWidget)
2. 右键点击 → `插入页面`
3. 自动创建新页面
4. 在新页面上添加组件

### 修改颜色主题
在 `MainWindow_ui.cpp` 的 `loadStyleSheet()` 函数中修改：

```cpp
// 修改这些颜色值
#1e1e1e  // 主窗口背景
#2d2d2d  // 菜单栏背景
#0078d4  // 主题蓝色
#e0e0e0  // 文字颜色
#252525  // 左侧导航背景
#0a0a0a  // 3D视口背景
```

## 📦 编译输出

编译成功后，可执行文件位置：
```
D:/Claude/fengchang/build-WindFieldRadar-Desktop_Qt_5_14_2_MinGW_32_bit-Debug/debug/WindFieldRadar.exe
```

## 🐛 常见问题

### Q1: 提示找不到 `ui_MainWindow.h`
**解决**：这是正常的，因为该文件在编译时自动生成。只需编译一次即可。

### Q2: 修改 .ui 文件后编译失败
**解决**：
1. 点击 `构建` → `全部清理`
2. 再次点击 `构建` → `构建全部`

### Q3: 界面显示不完整或变形
**解决**：
1. 检查窗口是否最大化
2. 调整窗口大小或重置布局

### Q4: 状态栏不显示时间
**解决**：
1. 检查 `onUpdateSystemTime()` 是否被正确调用
2. 确保定时器已启动

## 💡 进阶操作

### 自定义新组件
如果需要添加自定义组件（如 StatusIndicator）：

1. 在 Qt Designer 中选中一个普通 QWidget
2. 右键 → `提升为...`
3. 输入类名（如 `StatusIndicator`）
4. 输入头文件名（如 `StatusIndicator.h`）
5. 点击 `添加`
6. 保存 .ui 文件

### 调整布局间距
1. 在 Qt Designer 中选中布局
2. 在属性面板中调整 `spacing` 和 `margin`
3. 保存文件

### 修改默认选中页面
在 `setupUI()` 函数中修改：

```cpp
// 改变数字 0-7 来选择不同页面
ui->contentStack->setCurrentIndex(3);  // 0=系统总览, 1=设备控制, 3=三维可视化等
```

## 📚 相关文档

- [Qt 5.14 文档](https://doc.qt.io/qt-5.14/)
- [Qt Designer 用户手册](https://doc.qt.io/qt-5/qtdesigner-manual.html)
- [Qt Style Sheet 参考](https://doc.qt.io/qt-5/stylesheet-reference.html)

---

**最后更新**: 2026-07-29  
**版本**: v1.0 (UI 版本)
