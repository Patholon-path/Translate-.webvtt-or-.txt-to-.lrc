import re

def vtt_time_to_lrc_time(vtt_time):
    """
    将webvtt时间（如00:00:01.000）转换为lrc时间（如[00:01.00]）
    """
    # 只取分钟和秒，毫秒取前两位
    match = re.match(r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})", vtt_time)
    if not match:
        return None
    h, m, s, ms = match.groups()
    total_min = int(h) * 60 + int(m)
    # 毫秒转为小数点后两位
    lrc_time = f"[{total_min:02d}:{int(s):02d}.{ms[:2]}]"
    return lrc_time

def vtt_to_lrc(vtt_path, lrc_path):
    """
    读取vtt文件，转换为lrc格式并写入lrc文件
    """
    with open(vtt_path, 'r', encoding='utf-8') as fin, open(lrc_path, 'w', encoding='utf-8') as fout:
        lines = fin.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # 匹配时间轴行
            if re.match(r"\d{2}:\d{2}:\d{2}\.\d{3} -->", line):
                start_time = line.split(' ')[0]
                lrc_time = vtt_time_to_lrc_time(start_time)
                # 下一行是字幕内容
                i += 1
                while i < len(lines) and lines[i].strip() == "":
                    i += 1  # 跳过空行
                if i < len(lines):
                    lyric = lines[i].strip()
                    if lrc_time and lyric:
                        fout.write(f"{lrc_time}{lyric}\n")
            i += 1

if __name__ == "__main__":
    # 示例用法：python vtt_to_lrc.py input.vtt output.lrc
    import sys
    if len(sys.argv) != 3:
        print("用法: python vtt_to_lrc.py 输入文件.vtt 输出文件.lrc")
    else:
        vtt_to_lrc(sys.argv[1], sys.argv[2])
