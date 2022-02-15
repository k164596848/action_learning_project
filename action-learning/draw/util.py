from PIL import ImageDraw, ImageFont

font = ImageFont.truetype("./data/NotoSansCJKtc-Regular.otf", 48) 


def text_with_border(
    draw: ImageDraw, xy, text, font=font, fillcolor="white", shadowcolor="black",
):
    """Draw text with border."""
    # thin border
    draw.text((xy[0] - 1, xy[1]), text, font=font, fill=shadowcolor)
    draw.text((xy[0] + 1, xy[1]), text, font=font, fill=shadowcolor)
    draw.text((xy[0], xy[1] - 1), text, font=font, fill=shadowcolor)
    draw.text((xy[0], xy[1] + 1), text, font=font, fill=shadowcolor)

    # thicker border
    draw.text((xy[0] - 1, xy[1] - 1), text, font=font, fill=shadowcolor)
    draw.text((xy[0] + 1, xy[1] - 1), text, font=font, fill=shadowcolor)
    draw.text((xy[0] - 1, xy[1] + 1), text, font=font, fill=shadowcolor)
    draw.text((xy[0] + 1, xy[1] + 1), text, font=font, fill=shadowcolor)

    # now draw the text over it
    draw.text((xy[0], xy[1]), text, font=font, fill=fillcolor)
