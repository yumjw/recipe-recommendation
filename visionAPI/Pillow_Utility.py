#referred to Jie Jenn's code on his youtube video

from PIL import Image, ImageDraw, Image, ImageFont #pip install Pillow


def draw_borders(pillow_image, bounding, color, image_size, caption = '', confidence_score=0):

    width, height = image_size
    draw = ImageDraw.Draw(pillow_image)
    draw.polygon([
        bounding.normalized_vertices[0].x *
        width, bounding.normalized_vertices[0].y * height,
        bounding.normalized_vertices[1].x *
        width, bounding.normalized_vertices[1].y * height,
        bounding.normalized_vertices[2].x *
        width, bounding.normalized_vertices[2].y * height,
        bounding.normalized_vertices[3].x * width, bounding.normalized_vertices[3].y * height], fill=None, outline=color)

    font_size = width * height // 22000 if width * height > 400000 else 12

    font = ImageFont.truetype(r'/System/Library/Fonts/Monaco.dfont', 22) #input font u want to use 

    draw.text((bounding.normalized_vertices[0].x * width,
               bounding.normalized_vertices[0].y * height), font = font, text = caption, fill=color)

    draw.text((bounding.normalized_vertices[0].x * width, bounding.normalized_vertices[0].y *
               height * 20), font = font, text = 'confidence Score: {0:.2f}%'.format(confidence_score), fill=color)

    return pillow_image
