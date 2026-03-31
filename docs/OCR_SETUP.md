# 教材OCR提取指南

## 1. 安装Tesseract OCR引擎

### Windows系统

#### 方法1：使用winget（推荐，需要管理员权限）
```powershell
winget install UB-Mannheim.Tesseract
```

#### 方法2：手动下载安装
1. 下载地址：https://github.com/UB-Mannheim/tesseract/wiki
2. 下载最新的Windows安装包（如 `tesseract-ocr-w64-setup-5.x.x.exe`）
3. 运行安装程序，**记住安装路径**（通常是 `C:\Program Files\Tesseract-OCR`）
4. 在安装时勾选西班牙语和中文简体语言包

### 安装后配置

将Tesseract添加到系统PATH：
1. 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
2. 在"系统变量"中找到"Path"，点击编辑
3. 添加新条目：`C:\Program Files\Tesseract-OCR`（或你的安装路径）
4. 确定保存

### 验证安装

打开PowerShell，运行：
```powershell
tesseract --version
```

应该看到类似输出：
```
tesseract 5.x.x
 leptonica-1.x.x
  libgif 5.x.x : libjpeg 8.x (libjpeg-turbo 2.x.x) : libpng 1.x.x : libtiff 4.x.x : zlib 1.x.x : libwebp 1.x.x
 Found AVX512BW
 Found AVX512F
 Found AVX512VNNI
 Found AVX2
 Found AVX
 Found FMA
 Found SSE4.1
 Found OpenMP
 Found libarchive 3.x.x
 Found libcurl/7.x.x-SSL
 Found ZSTD
```

## 2. 下载语言包

如果安装时没有勾选语言包，需要手动下载：
1. 访问：https://github.com/tesseract-ocr/tessdata
2. 下载 `spa.traineddata`（西班牙语）和 `chi_sim.traineddata`（中文简体）
3. 将文件复制到Tesseract安装目录的 `tessdata` 文件夹：
   ```
   C:\Program Files\Tesseract-OCR\tessdata\
   ```

## 3. 运行OCR提取脚本

安装完成后，运行：
```powershell
cd d:/2026-03-31_AITeacher/backend
python extract_textbook_ocr.py
```

提取的文本会保存到：`d:/2026-03-31_AITeacher/course/textbook_extract.txt`

## 4. 常见问题

### 问题1：`TesseractNotFoundError: tesseract is not installed`
**解决**：检查PATH是否正确添加，重启PowerShell

### 问题2：识别准确率低
**解决**：
- 尝试提高PDF扫描分辨率（如果有原文件）
- 使用 `--psm` 参数调整页面分割模式
- 使用 `--oem` 参数选择OCR引擎

### 问题3：提取的文本格式混乱
**解决**：
- OCR提取后需要人工校对和格式化
- 建议先提取，再整理成结构化内容

## 5. OCR优化建议

### 提高准确率的参数
```python
# 使用PSM 6（假设单列文本）
text = pytesseract.image_to_string(image, lang='spa', config='--psm 6')

# 使用OEM 3（基于LSTM的默认OCR引擎）
text = pytesseract.image_to_string(image, lang='spa', config='--oem 3')
```

### 多语言识别
```python
# 同时使用西班牙语和中文
text = pytesseract.image_to_string(image, lang='spa+chi_sim')
```

---

**下一步**：安装完成后运行OCR脚本，提取教材内容。
