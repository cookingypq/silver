# SILVER Frontend

SILVER RustSec Analyzer的前端界面，使用React和8-bit风格UI组件构建。

## 功能特性

- 🎮 8-bit复古风格UI设计
- 📱 响应式设计，支持各种屏幕尺寸
- 🔍 实时搜索和过滤功能
- 📊 结果可视化展示
- 📤 支持JSON和TXT格式导出
- ⚡ 使用Vite构建，快速开发体验

## 技术栈

- React 19
- Vite
- 8-bit风格组件库
- Framer Motion (动画)

## 快速开始

### 使用 Bun (推荐)

```bash
# 安装依赖
bun install

# 启动开发服务器
bun run dev

# 构建生产版本
bun run build

# 预览生产版本
bun run preview
```

### 使用 npm

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

## 开发服务器

启动后访问: http://localhost:5173/

## 8-bit组件

项目包含以下8-bit风格组件：

- `BitButton` - 8-bit风格按钮
- `BitCard` - 8-bit风格卡片
- `BitInput` - 8-bit风格输入框
- `BitLabel` - 8-bit风格标签

所有组件都支持响应式设计和像素化边框效果。

## 响应式设计

- 桌面端: 1200px+
- 平板端: 768px - 1199px
- 手机端: 480px - 767px
- 小屏手机: < 480px

## 构建和部署

```bash
# 构建生产版本
bun run build

# 预览构建结果
bun run preview
```

构建后的文件将生成在 `dist/` 目录中。
