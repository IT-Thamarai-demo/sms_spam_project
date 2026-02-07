from PIL import Image, ImageDraw, ImageFont
import os

def create_screenshot(name, title, prediction, risk, confidence, keywords, risk_color):
    # Mobile frame dimensions
    width, height = 360, 740
    img = Image.new('RGB', (width, height), color='#F5F5F5')
    draw = ImageDraw.Draw(img)
    
    # Status bar
    draw.rectangle([0, 0, width, 30], fill='black')
    
    # App Bar
    draw.rectangle([0, 30, width, 90], fill='#6200EE')
    # Use default font or try to find a ttf
    font = ImageFont.load_default()
    draw.text((16, 45), "SMS Classifier", fill='white', font=font)
    
    # Main Card
    draw.rounded_rectangle([16, 110, width-16, 250], radius=12, fill='white', outline='#ddd', width=1)
    draw.text((32, 126), "Paste SMS message here...", fill='#999', font=font)
    draw.rectangle([32, 142, width-32, 200], outline='#eee') # Text box
    
    # Button
    draw.rounded_rectangle([32, 210, width-32, 240], radius=6, fill='#6200EE')
    draw.text((140, 218), "Scan Message", fill='white', font=font)
    
    # Result Card (if applicable)
    if prediction:
        draw.rounded_rectangle([16, 266, width-16, 450], radius=12, fill='white', outline='#ddd', width=1)
        # Risk Badge
        draw.rounded_rectangle([32, 282, 120, 302], radius=10, fill=risk_color)
        draw.text((40, 286), f"Risk: {risk}", fill='white', font=font)
        
        # Prediction
        draw.text((32, 310), prediction, fill=risk_color, font=font)
        
        # Details
        draw.text((32, 360), f"Confidence: {confidence}", fill='#333', font=font)
        draw.text((32, 385), f"Keywords: {keywords}", fill='#6200EE', font=font)
    
    # Save to current dir
    save_path = f"c:/Users/Asus/Desktop/smstrain/sms_spam_project/{name}.png"
    img.save(save_path)
    print(f"Saved {save_path}")

if __name__ == "__main__":
    # 1. Dashboard
    create_screenshot("mock_dashboard", "", "", "", "", "", "")
    
    # 2. Phishing Result
    create_screenshot("mock_phishing_result", "Result", "Spam", "High", "99.99%", "suspended, urgent, verify", "#E91E63")
    
    # 3. Ham Result
    create_screenshot("mock_ham_result", "Result", "Ham", "Low", "100.00%", "lunch, meeting, let", "#4CAF50")
