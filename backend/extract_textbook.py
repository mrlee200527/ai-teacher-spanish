"""提取教材文本内容（OCR版本）"""
from pdf2image import convert_from_path
import pytesseract
import sys

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pdf_path = r"D:/文档/学习文档/西班牙语/Santy西班牙语/速成西班牙语(第1册).pdf"

print("=" * 60)
print("速成西班牙语教材提取（OCR）")
print("=" * 60)

try:
    print("\n[检查Tesseract OCR...]")
    try:
        pytesseract.get_tesseract_version()
        print(f"[OK] Tesseract版本: {pytesseract.get_tesseract_version()}")
    except Exception as e:
        print(f"[ERROR] Tesseract未安装或配置不正确")
        print(f"请安装Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki")
        sys.exit(1)
    
    print("\n[开始提取前5课内容（前10页）...]")
    print("警告：OCR可能需要较长时间，请耐心等待...")
    
    # 将PDF转换为图像
    images = convert_from_path(pdf_path, first_page=1, last_page=10)
    print(f"[OK] 转换了 {len(images)} 页图像")
    
    # OCR识别
    all_text = ""
    for i, image in enumerate(images):
        print(f"[{i+1}/{len(images)}] 正在识别第 {i+1} 页...")
        text = pytesseract.image_to_string(image, lang='spa+chi_sim')
        all_text += f"\n\n{'='*60}\n"
        all_text += f"第 {i+1} 页\n"
        all_text += f"{'='*60}\n"
        all_text += text
    
    # 保存到文件
    output_file = "d:/2026-03-31_AITeacher/course/textbook_extract.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    print(f"\n[OK] 内容已保存到: {output_file}")
    print(f"\n提取文本长度: {len(all_text)} 字符")
    
    # 显示预览
    preview = all_text[:800] if len(all_text) > 800 else all_text
    print(f"\n内容预览:")
    print("-" * 60)
    print(preview)
    print("..." if len(all_text) > 800 else "")
    
except FileNotFoundError:
    print(f"[ERROR] PDF文件不存在: {pdf_path}")
except Exception as e:
    print(f"[ERROR] 提取失败: {e}")
    import traceback
    traceback.print_exc()
