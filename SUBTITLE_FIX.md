# 字幕面板滚动优化说明

## 修复的问题

1. **字幕栏跳动** - 字幕切换时滚动条不稳定
2. **高亮闪烁** - 当前字幕高亮状态频繁变化
3. **用户滚动冲突** - 用户手动滚动时被自动滚动打断

## 实现的优化

### 1. 防重复高亮机制
```python
self.current_highlight_id = None  # 跟踪当前高亮的字幕ID

# 只在字幕ID变化时才更新高亮
if segment and segment.id == self.current_highlight_id:
    return
```

**效果**: 避免同一字幕反复高亮，减少闪烁

### 2. 智能滚动控制
```python
self.scroll_enabled = True      # 允许/禁止自动滚动
self.user_scrolling = False     # 检测用户是否在滚动
```

**效果**:
- 用户手动滚动时，暂停自动滚动500ms
- 点击字幕跳转时，临时禁用自动滚动

### 3. 滚动频率限制
```python
self.last_scroll_time = 0
self.scroll_threshold = 100  # 100ms最小间隔

# 检查滚动频率
if current_time - self.last_scroll_time < self.scroll_threshold:
    return
```

**效果**: 避免过于频繁的滚动操作，平滑滚动体验

### 4. 智能滚动位置
```python
# 将目标字幕放在视口中央
target_position = widget_top - (viewport_height // 2) + (widget_height // 2)

# 确保位置在有效范围内
target_position = max(min_value, min(target_position, max_value))
```

**效果**:
- 当前字幕始终显示在视野中央
- 上下各有几条字幕可见，方便预览

### 5. 用户滚动检测
```python
def _on_scroll_changed(self, value: int):
    # 用户滚动时暂停自动滚动
    self.user_scrolling = True
    # 500ms后恢复
    QTimer.singleShot(500, self._enable_auto_scroll)
```

**效果**: 用户手动查看字幕时，不会被打断

## 使用体验

### 播放视频时
- ✓ 当前播放字幕自动高亮
- ✓ 字幕面板自动滚动，当前字幕居中显示
- ✓ 滚动平滑，无跳动
- ✓ 上下字幕可见，方便预览

### 点击字幕时
- ✓ 视频跳转到对应时间
- ✓ 字幕面板滚动到目标位置
- ✓ 目标字幕高亮显示
- ✓ 500ms后恢复自动跟随

### 用户手动滚动时
- ✓ 自动滚动暂停
- ✓ 用户可以自由浏览所有字幕
- ✓ 500ms后自动恢复播放跟随

## 技术细节

### 更新频率
- 定时器间隔: 100ms (主窗口)
- 滚动间隔阈值: 100ms
- 用户滚动恢复: 500ms

### 性能优化
- 字幕未变化时跳过高亮更新
- 限制滚动频率避免过度重绘
- 使用几何计算确保精确滚动位置

### 边界处理
- 滚动位置限制在有效范围内
- 空字幕列表时安全处理
- widget未创建时的异常处理

## 配置参数

可以根据需要调整以下参数：

```python
# 在 SubtitlePanel.__init__ 中

# 滚动间隔阈值（毫秒）- 越小滚动越频繁，但可能更耗资源
self.scroll_threshold = 100

# 用户滚动恢复时间（毫秒）- 越长恢复自动跟随越慢
QTimer.singleShot(500, ...)
```

## 测试建议

1. **播放测试**: 播放视频，观察字幕高亮和滚动是否流畅
2. **跳转测试**: 点击不同字幕，验证跳转和滚动是否准确
3. **手动滚动测试**: 用户手动滚动后，验证自动跟随是否正确恢复
4. **长时间测试**: 播放长视频，验证无内存泄漏和性能下降
