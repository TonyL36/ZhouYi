import re
import os

def parse_zhouyi_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by "## 第"
    # Note: ZhouYi.md uses "## 第1卦", "## 第2卦"...
    # But some might be "## 第51卦 震"
    
    # We mainly want to extract Image and Binary Code for each Hexagram Number.
    hex_data = {}
    
    # Regex to find blocks. 
    # We look for "## 第(\d+)卦"
    # Note: Using finditer with lookahead might be tricky if the file structure varies.
    # Let's use split instead, similar to text parser.
    
    segments = re.split(r'(?=## 第\d+卦)', content)
    
    print(f"DEBUG: Found {len(segments)} segments in ZhouYi.md")
    
    for block in segments:
        if not block.strip().startswith("## 第"):
            continue
            
        # Extract Seq
        seq_match = re.match(r'## 第(\d+)卦', block.strip())
        if not seq_match:
            continue
            
        seq = int(seq_match.group(1))
        
        # Extract Image
        img_match = re.search(r'!\[.*?\]\((.*?)\)', block)
        img_src = img_match.group(1) if img_match else ""
        
        # Extract Code
        code_match = re.search(r'\*\*卦象编码\*\*：([01]+)', block)
        code = code_match.group(1) if code_match else ""
        
        if seq == 1:
            print(f"DEBUG: Hex 1 Block: {block[:100]}...")
            print(f"DEBUG: Hex 1 Image: {img_src}")
            print(f"DEBUG: Hex 1 Code: {code}")
            
        if seq not in hex_data:
            hex_data[seq] = {
                'image': img_src,
                'code': code
            }
            
    
    # Pre-defined Hexagram Data (King Wen Sequence)
    # Binary Code: 1=Yang, 0=Yin, Bottom->Top
    hex_ref_data = {
        1: {'code': '111111', 'name': '乾'},
        2: {'code': '000000', 'name': '坤'},
        3: {'code': '100010', 'name': '屯'},
        4: {'code': '010001', 'name': '蒙'},
        5: {'code': '111010', 'name': '需'},
        6: {'code': '010111', 'name': '讼'},
        7: {'code': '010000', 'name': '师'},
        8: {'code': '000010', 'name': '比'},
        9: {'code': '111011', 'name': '小畜'},
        10: {'code': '110111', 'name': '履'},
        11: {'code': '111000', 'name': '泰'},
        12: {'code': '000111', 'name': '否'},
        13: {'code': '101111', 'name': '同人'},
        14: {'code': '111101', 'name': '大有'},
        15: {'code': '001000', 'name': '谦'},
        16: {'code': '000100', 'name': '豫'},
        17: {'code': '100110', 'name': '随'},
        18: {'code': '011001', 'name': '蛊'},
        19: {'code': '110000', 'name': '临'},
        20: {'code': '000011', 'name': '观'},
        21: {'code': '100101', 'name': '噬嗑'},
        22: {'code': '101001', 'name': '贲'},
        23: {'code': '000001', 'name': '剥'},
        24: {'code': '100000', 'name': '复'},
        25: {'code': '100111', 'name': '无妄'},
        26: {'code': '111001', 'name': '大畜'},
        27: {'code': '100001', 'name': '颐'},
        28: {'code': '011110', 'name': '大过'},
        29: {'code': '010010', 'name': '坎'},
        30: {'code': '101101', 'name': '离'},
        31: {'code': '001110', 'name': '咸'},
        32: {'code': '011100', 'name': '恒'},
        33: {'code': '001111', 'name': '遁'},
        34: {'code': '111100', 'name': '大壮'},
        35: {'code': '000101', 'name': '晋'},
        36: {'code': '101000', 'name': '明夷'},
        37: {'code': '101011', 'name': '家人'},
        38: {'code': '110101', 'name': '睽'},
        39: {'code': '001010', 'name': '蹇'},
        40: {'code': '010100', 'name': '解'},
        41: {'code': '110001', 'name': '损'},
        42: {'code': '100011', 'name': '益'},
        43: {'code': '111110', 'name': '夬'},
        44: {'code': '011111', 'name': '姤'},
        45: {'code': '000110', 'name': '萃'},
        46: {'code': '011000', 'name': '升'},
        47: {'code': '010110', 'name': '困'},
        48: {'code': '011010', 'name': '井'},
        49: {'code': '101110', 'name': '革'},
        50: {'code': '011101', 'name': '鼎'},
        51: {'code': '100100', 'name': '震'},
        52: {'code': '001001', 'name': '艮'},
        53: {'code': '001011', 'name': '渐'},
        54: {'code': '110100', 'name': '归妹'},
        55: {'code': '101100', 'name': '丰'},
        56: {'code': '001101', 'name': '旅'},
        57: {'code': '011011', 'name': '巽'},
        58: {'code': '110110', 'name': '兑'},
        59: {'code': '010011', 'name': '涣'},
        60: {'code': '110010', 'name': '节'},
        61: {'code': '110011', 'name': '中孚'},
        62: {'code': '001100', 'name': '小过'},
        63: {'code': '101010', 'name': '既济'},
        64: {'code': '010101', 'name': '未济'}
    }
    
    # Merge extracted data with reference data
    # If extraction failed (image/code missing), use reference
    for seq, ref in hex_ref_data.items():
        if seq not in hex_data:
            hex_data[seq] = {'image': '', 'code': ''}
            
        if not hex_data[seq]['code']:
            hex_data[seq]['code'] = ref['code']
            
        # Ensure Image Path starts with / for absolute path on server
        # This fixes the relative path issue in frontend (src="images/..." vs src="/images/...")
        img_path = hex_data[seq]['image']
        if not img_path:
             img_path = f"images/{seq:02d}_{ref['name']}.svg"
        
        if not img_path.startswith('/'):
            img_path = '/' + img_path
            
        hex_data[seq]['image'] = img_path
            
    return hex_data

def parse_text_source(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Pre-process: Join lines, but keep delimiters.
    # The file has "->" arrows which seem to be line numbers or markers from a reader.
    # The read output showed "1->" etc. 
    # Wait, the read output format from the tool `cat -n` added those arrows? 
    # No, the tool output was `1→...`. The file content itself likely doesn't have them if it's a normal text file, 
    # OR the tool added them.
    # Let's assume the file content is normal text. I will check the file content again or assume standard text.
    # The previous `Read` output had `1→...`. This looks like the `cat` tool output formatting.
    # Let's verify if the file has line numbers. The tool description says "Results are returned using cat -n format".
    # So the arrows and numbers are artifacts of the tool, NOT the file.
    # I should treat the file as normal text.
    
    full_text = "".join(lines)
    
    # Split by "# 第"
    # The source has "# 第一卦", "# 第二卦"...
    # Regex: # 第[一二三四五六七八九十]+卦
    
    segments = re.split(r'(?=# 第[一二三四五六七八九十]+卦)', full_text)
    
    parsed_data = {}
    
    chinese_num_map = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
    }
    
    def cn_to_int(cn_str):
        # Simple parser for 1-64
        if not cn_str: return 0
        if len(cn_str) == 1: return chinese_num_map.get(cn_str, 0)
        if len(cn_str) == 2:
            if cn_str[0] == '十': return 10 + chinese_num_map.get(cn_str[1], 0)
            if cn_str[1] == '十': return chinese_num_map.get(cn_str[0], 0) * 10
        if len(cn_str) == 3:
             # e.g. 五十八
             if cn_str[1] == '十':
                 return chinese_num_map.get(cn_str[0], 0) * 10 + chinese_num_map.get(cn_str[2], 0)
        return 0

    for segment in segments:
        if not segment.strip():
            continue
            
        lines = segment.strip().split('\n')
        title_line = lines[0].strip()
        
        # Extract Number from Title
        # Format: # 第四十九卦 革 泽火革 兑上离下
        # Sometimes missing space: # 第五十一卦震
        title_match = re.match(r'# 第([一二三四五六七八九十]+)卦\s*(.*)', title_line)
        if not title_match:
            continue
            
        num_cn = title_match.group(1)
        seq = cn_to_int(num_cn)
        rest_of_title = title_match.group(2)
        
        # Clean Title: The user wants "第X卦 [Name] [Full Name] [Structure]" but with Arabic numerals for backend compatibility.
        # Backend regex: ## 第(\d+)卦 (\S+)
        # So we must use: ## 第{seq}卦 {rest_of_title}
        # But we need to make sure {rest_of_title} starts with the Name.
        # In the file: "革 泽火革 兑上离下". Correct.
        # In "第五十一卦震": rest is "震". Correct.
        
        clean_title = f"第{seq}卦 {rest_of_title}"
        
        # Parse Body
        body = "\n".join(lines[1:])
        
        # Extract Sections
        # Patterns:
        # Guaci: Starts at beginning of body, ends at "彖曰"
        # Tuan: Starts with "彖曰"
        # Xiang: Starts with "象曰" (The main one)
        # Yao: Starts with "初[六九]" etc.
        
        # Let's normalize newlines
        body = body.replace('\r\n', '\n')
        
        # Find Tuan
        tuan_start = body.find('彖曰')
        if tuan_start == -1:
            # Fallback or error
            guaci = body
            tuan = ""
            xiang = ""
            yao_text = "" # Fallback
        else:
            guaci = body[:tuan_start].strip()
            # Find Xiang
            xiang_start = body.find('象曰', tuan_start + 1)
            
            # Note: Yao lines also have "象曰". The Great Xiang usually comes before Yao lines.
            
            if xiang_start != -1:
                tuan = body[tuan_start:xiang_start].strip()
                
                # Where do Yao lines start?
                # Look for first occurrence of "初[六九]" etc followed by colon
                yao_pattern = re.compile(r'(初[六九]|六[二三四五]|九[二三四五]|上[六九]|用[六九])[：:]')
                yao_match = yao_pattern.search(body, xiang_start)
                
                if yao_match:
                    yao_start_idx = yao_match.start()
                    xiang = body[xiang_start:yao_start_idx].strip()
                    yao_text = body[yao_start_idx:]
                else:
                    xiang = body[xiang_start:].strip()
                    yao_text = ""
            else:
                tuan = body[tuan_start:].strip()
                xiang = ""
                yao_text = ""
        
        # Check if Guaci contains Yao lines (Hexagram 1 case)
        # If yao_text is empty, check guaci
        if not yao_text:
             yao_pattern = re.compile(r'(初[六九]|六[二三四五]|九[二三四五]|上[六九]|用[六九])[：:]')
             yao_match_in_guaci = yao_pattern.search(guaci)
             if yao_match_in_guaci:
                 print(f"DEBUG: Found Yao lines in Guaci for Hex {seq}")
                 yao_start_idx = yao_match_in_guaci.start()
                 yao_text = guaci[yao_start_idx:]
                 guaci = guaci[:yao_start_idx].strip()

        # Parse Yao Lines
                
        # Parse Yao Lines
        # Yao lines are: Title (e.g. 初九：...) then maybe 象曰 on same or next line.
        # We want to format them as bullets.
        
        yao_lines = []
        if yao_text:
            # Normalize "象 曰" to "象曰"
            yao_text = yao_text.replace('象 曰', '象曰')
            
            # Split by the keywords with colon
            # We can use split with capturing group to keep delimiters (the key)
            parts = yao_pattern.split(yao_text)
            # parts[0] is empty or whitespace
            # parts[1] is keyword (e.g. 初九), parts[2] is content (colon is consumed)
            # parts[3] is keyword, parts[4] is content...
            
            for i in range(1, len(parts), 2):
                y_key = parts[i]
                y_content = parts[i+1] if i+1 < len(parts) else ""
                
                # Check for "象曰" in content
                y_xiang = ""
                y_xiang_idx = y_content.find('象曰')
                if y_xiang_idx != -1:
                    y_xiang = y_content[y_xiang_idx:].strip()
                    y_content = y_content[:y_xiang_idx].strip()
                
                # Remove colons or extra spaces from key/content
                y_content = y_content.lstrip('：:').strip()
                
                yao_lines.append({
                    'title': y_key,
                    'content': y_content,
                    'xiang': y_xiang
                })
        
        parsed_data[seq] = {
            'title': clean_title,
            'guaci': guaci,
            'tuan': tuan,
            'xiang': xiang,
            'yaos': yao_lines
        }
        
    return parsed_data

def generate_markdown(hex_md_data, text_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write Header
        f.write("# 周易全文\n\n")
        f.write("本文件包含周易六十四卦的卦象图片和卦名。\n\n")
        f.write("## 目录\n\n")
        
        # Write TOC
        for i in range(1, 65):
            if i in text_data:
                # TOC Format: - [1. 乾](#第1卦-乾)
                # But the anchor depends on the header.
                # New header format: ## 第X卦 Name ...
                # Let's keep a simple TOC or generate based on new titles.
                # User wants "title写成这种格式...".
                # Let's use the full title in TOC? Or keep it simple?
                # The original TOC was "- [1. 乾](#第1卦-乾)".
                # The headers were "## 第1卦 乾".
                # If we change header to "## 第四十九卦 革...", the anchor changes.
                # Let's use the simple name for TOC if possible, but we might not have it separated easily.
                # Actually, the text data title is "第四十九卦 革 泽火革 兑上离下".
                # We can extract the name "革".
                parts = text_data[i]['title'].split(' ')
                short_name = parts[1] if len(parts) > 1 else ""
                
                # Anchor generation is tricky with Chinese.
                # Let's try to stick to a standard TOC format.
                f.write(f"- [{i}. {short_name}](#{text_data[i]['title'].replace(' ', '-')})\n")
        
        f.write("\n---\n\n")
        
        for i in range(1, 65):
            if i not in text_data:
                print(f"Missing text for Hexagram {i}")
                continue
                
            t_data = text_data[i]
            m_data = hex_md_data.get(i, {'image': '', 'code': ''})
            
            # Header
            f.write(f"## {t_data['title']}\n\n")
            
            # Image
            if m_data['image']:
                f.write('<div align="center">\n\n')
                f.write(f"![{t_data['title'].split(' ')[1]}]({m_data['image']})\n\n")
                f.write('</div>\n\n')
            
            # Code
            if m_data['code']:
                # Determine binary meaning (Initial -> Top)
                f.write(f"**卦象编码**：{m_data['code']}（初爻 -> 上爻）\n\n")
            
            # Guaci
            f.write("> **卦辞**：\n>\n")
            f.write(f"> {t_data['guaci']}\n\n")
            
            # Tuan
            if t_data['tuan']:
                f.write("> **彖曰**：\n>\n")
                f.write(f"> {t_data['tuan']}\n\n")
            
            # Xiang
            if t_data['xiang']:
                f.write("> **象曰**：\n>\n")
                f.write(f"> {t_data['xiang']}\n\n")
            
            # Yaos
            for yao in t_data['yaos']:
                f.write(f"- **{yao['title']}**：{yao['content']}\n")
                if yao['xiang']:
                    # Clean up "象曰：" from the start if it exists, to match format
                    x_content = yao['xiang']
                    # original format: > *象曰：...*
                    f.write(f"  > *{x_content}*\n")
            
            f.write("\n---\n\n")

if __name__ == "__main__":
    base_dir = r"e:\GitProjects\MyProject\ZhouYi"
    md_path = os.path.join(base_dir, r"backend\src\main\resources\data\ZhouYi.md")
    txt_path = os.path.join(base_dir, "认可度较高版本.txt")
    output_path = os.path.join(base_dir, r"backend\src\main\resources\data\ZhouYi_fixed.md")
    
    hex_data = parse_zhouyi_md(md_path)
    text_data = parse_text_source(txt_path)
    
    generate_markdown(hex_data, text_data, output_path)
    print(f"Generated {output_path}")
