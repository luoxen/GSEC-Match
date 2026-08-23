import qrcode
from PIL import Image
import os

# 应用 URL
url = "https://gsec-match-6mfu2rkkjxkqi8tgsqqoy6.streamlit.app"

# 创建二维码
qr = qrcode.QRCode(
    version=3,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # 使用高容错率，以便添加Logo
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# 生成二维码图片
img = qr.make_image(fill_color="#1f77b4", back_color="white").convert('RGB')

# 添加Logo
logo_path = "/Users/Admin/Documents/运动营养+抗衰老/中考体育/GSEC-Match/学会会标.png"

try:
    if os.path.exists(logo_path):
        # 打开Logo并调整大小
        logo = Image.open(logo_path)
        
        # 计算Logo大小（二维码的1/5）
        img_w, img_h = img.size
        logo_size = img_w // 5
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # 计算居中位置
        logo_w, logo_h = logo.size
        pos = ((img_w - logo_w) // 2, (img_h - logo_h) // 2)
        
        # 如果Logo有透明通道，使用它作为蒙版
        if logo.mode == 'RGBA':
            img.paste(logo, pos, logo)
        else:
            # 如果没有透明通道，创建白色背景
            white_bg = Image.new('RGBA', (logo_w, logo_h), (255, 255, 255, 255))
            white_bg.paste(logo, (0, 0))
            img.paste(white_bg, pos, white_bg)
        
        print("✅ 带Logo的二维码已生成！")
    else:
        print(f"⚠️ Logo文件不存在: {logo_path}")
        print("✅ 已生成普通二维码（无Logo）")
except Exception as e:
    print(f"⚠️ 添加Logo时出错: {e}")
    print("✅ 已生成普通二维码（无Logo）")

# 保存图片
img.save("GSEC-Match_QR_With_Logo.png")
print("📱 二维码文件: GSEC-Match_QR_With_Logo.png")
print(f"🔗 应用地址: {url}")
print("📋 使用手机扫描二维码即可访问应用")
