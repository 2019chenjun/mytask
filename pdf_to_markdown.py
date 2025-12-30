import PyPDF2
import argparse
import os
from typing import List

def extract_text_from_pdf(pdf_path: str) -> List[str]:
    """从PDF文件中提取文本"""
    with open(pdf_path, 'rb') as file:
        # 创建PDF阅读器对象
        pdf_reader = PyPDF2.PdfReader(file)
        text_content = []
        
        # 遍历所有页面
        for page in pdf_reader.pages:
            text_content.append(page.extract_text())
            
    return text_content

def convert_to_markdown(text_content: List[str]) -> str:
    """将提取的文本转换为Markdown格式"""
    markdown_content = []
    
    for page_num, page_text in enumerate(text_content, 1):
        # 添加页面标题
        markdown_content.append(f"## 第 {page_num} 页\n")
        
        # 处理文本内容
        lines = page_text.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                markdown_content.append(line + "\n\n")
                
    return "".join(markdown_content)

def pdf_to_markdown(pdf_path: str, output_path: str = None) -> None:
    """
    将PDF文件转换为Markdown文件
    :param pdf_path: PDF文件路径
    :param output_path: 输出Markdown文件路径（可选）
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"找不到PDF文件: {pdf_path}")
    
    # 处理输出路径
    if output_path:
        # 如果输出路径是目录，则在目录中使用原文件名
        if os.path.isdir(output_path):
            pdf_filename = os.path.basename(pdf_path)
            base_name = os.path.splitext(pdf_filename)[0]
            output_path = os.path.join(output_path, f"{base_name}.md")
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
    else:
        output_path = os.path.splitext(pdf_path)[0] + '.md'
    
    # 提取文本
    text_content = extract_text_from_pdf(pdf_path)
    
    # 转换为Markdown
    markdown_content = convert_to_markdown(text_content)
    
    # 保存Markdown文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"转换完成！输出文件: {output_path}")

def main():
    print("PDF转Markdown工具")
    parser = argparse.ArgumentParser(description='将PDF文件转换为Markdown格式')
    parser.add_argument('input', help='输入PDF文件路径')
    parser.add_argument('-o', '--output', help='输出Markdown文件路径（可选）')
    
    args = parser.parse_args()
    pdf_to_markdown(args.input, args.output)

if __name__ == "__main__":
    main()
