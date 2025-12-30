from colorist import ColorRGB, BgColorRGB

dusty_pink = BgColorRGB(0b11000011, 0b10010000, 0b10100101)
bg_steel_blue = BgColorRGB(70, 130, 180)

print(f"I want to use {dusty_pink}dusty pink{dusty_pink.OFF} and {bg_steel_blue}steel blue{bg_steel_blue.OFF} colors")   