from flask import Flask, render_template_string
import json
import markdown2

app = Flask(__name__)

@app.route('/')
def index():
    # 读取 JSON 文件
    with open('ChatGPT_Raw_conversation.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
  
    
    # 提取所有消息中的 'content' -> 'parts' 并在 'role' 为 'assistant' 后添加分隔线
    markdown_content = ""                                            # Json文件的结构message>{}value> {}author > role: string 和 message> {}value> {}content > []parts > abc  
    for message in data["messages"]:                                 # 循环遍历 JSON 数据中的每个messages，不过目前就只有一个messages
        if "content" in message and "parts" in message["content"]:   # 检查每个消息是否包含 content 键，并且该 content 是否包含 parts 键。
            parts_content = "\n".join(message["content"]["parts"])   # 将 parts 数组中的所有字符串元素合并为一个单独的字符串，每个部分之间用换行符 \n 分隔。
            markdown_content += parts_content                        # 将合并后的 parts 内容追加到 markdown_content 字符串。
            if message["author"]["role"] == "assistant":             # 判断message中，role的值。
                markdown_content += "\n\n---\n\n"  # Markdown 分隔线

    # 转换为 Markdown 字符串，将 Markdown 转换为 HTML
    html_content = markdown2.markdown(markdown_content)

    
    
    # 使用 Flask 的 render_template_string 功能来显示内容
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>对话内容</title>
    </head>
    <body>
        {{ html_content|safe }}
    </body>
    </html>
    """, html_content=html_content) # html_content 制定了输入的内容
        
if __name__ == '__main__':
    app.run(debug=True)
