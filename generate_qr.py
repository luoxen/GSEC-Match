import qrcode
from PIL import Image

# 应用 URL
url = "https://gsec-match-6mfu2rkkjxkqi8tgsqqoy6.streamlit.app"

# 创建二维码
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# 生成图片
img = qr.make_image(fill_color="black", back_color="white")
img.save("GSEC-Match_QR.png")

print("✅ 二维码已生成: GSEC-Match_QR.png")
print(f"📱 扫描二维码访问: {url}")
