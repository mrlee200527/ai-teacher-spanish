"""使用OCR提取教材文本内容"""
from pdf2image import convert_from_path
import pytesseract
import sys
import os

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pdf_path = r"D:/文档/学习文档/西班牙语/Santy西班牙语/速成西班牙语(第1册).pdf"
output_file = "d:/2026-03-31_AITeacher/course/textbook_extract.txt"

print("=" * 60)
print("速成西班牙语教材提取（OCR）")
print("=" * 60)

try:
    # 检查Tesseract是否安装
    print("\n[检查Tesseract OCR...]")
    try:
        pytesseract.get_tesseract_version()
        print(f"[OK] Tesseract版本: {pytesseract.get_tesseract_version()}")
    except Exception as e:
        print(f"[ERROR] Tesseract未安装或配置不正确")
        print(f"错误信息: {e}")
        print(f"\n请按照 docs/OCR_SETUP.md 安装Tesseract OCR")
        sys.exit(1)
    
    # 检查PDF文件
    if not os.path.exists(pdf_path):
        print(f"[ERROR] PDF文件不存在: {pdf_path}")
        sys.exit(1)
    
    # 获取总页数
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"[OK] PDF总页数: {total_pages}")
    
    # 提取前5课内容（假设前20页）
    print("\n[开始提取前5课内容（前20页）...]")
    print("警告：OCR可能需要较长时间，请耐心等待...")
    print("预计时间：2-5分钟\n")
    
    # 将PDF转换为图像（逐页处理，节省内存）
    all_text = ""
    
    for page_num in range(1, 21):  # 前20页
        print(f"[{page_num}/20] 正在提取第 {page_num} 页...")
        
        try:
            # 转换单页为图像
            images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num)
            
            if images:
                image = images[0]
                
                # OCR识别（使用西班牙语和中文）
                # --psm 6: 假设单列文本
                # --oem 3: 使用LSTM引擎
                custom_config = r'--psm 6 --oem 3'
                text = pytesseract.image_to_string(image, lang='spa+chi_sim', config=custom_config)
                
                all_text += f"\n\n{'='*60}\n"
                all_text += f"第 {page_num} 页\n"
                all_text += f"{'='*60}\n"
                all_text += text
                
                print(f"  ✓ 提取完成，文本长度: {len(text)} 字符")
            else:
                print(f"  ✗ 第 {page_num} 页转换失败")
        
        except Exception as e:
            print(f"  ✗ 第 {page_num} 页处理失败: {e}")
    
    # 保存到文件
    print(f"\n[保存提取内容...]")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    print(f"\n[OK] 内容已保存到: {output_file}")
    print(f"[OK] 提取文本总长度: {len(all_text)} 字符")
    
    # 显示预览
    preview_length = 1000 if len(all_text) > 1000 else len(all_text)
    print(f"\n内容预览（前 {preview_length} 字符）:")
    print("-" * 60)
    print(all_text[:preview_length])
    print("..." if len(all_text) > preview_length else "")
    
    print("\n" + "=" * 60)
    print("提取完成！")
    print("=" * 60)
    print("\n下一步：")
    print("1. 检查提取的文本（必要时人工校对）")
    print("2. 整理内容，提取前5课结构")
    print("3. 使用脚本转换为课程格式")
    
except FileNotFoundError:
    print(f"[ERROR] PDF文件不存在: {pdf_path}")
except Exception as e:
    print(f"[ERROR] 提取失败: {e}")
    import traceback
    traceback.print_exc()
