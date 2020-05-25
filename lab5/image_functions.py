from PIL import Image
from numpy import array


n_coords = (308, 278, 317, 289)
t_coords = (393, 210, 399, 223)
e_coords = (401, 213, 409, 223)
x_coords = (411, 213, 420, 223)
pattern_coords = (427, 495, 528, 514)


def image_to_binary_array(image: Image):
    converted_image = image.convert(mode='P', palette=Image.ADAPTIVE)
    return array(converted_image)


def get_image(source):
    return Image.open(source)


def get_and_prepare_image(source):
    return image_to_binary_array(get_image(source))


def get_data(left, upper, right, lower, array_image):
    data = []
    for row in array_image[upper:lower]:
        data.append(row[left:right])
    return data


def get_letters_image(source):
    image = get_image(source)

    pattern1 = image.crop(n_coords)
    pattern1.save('n.png')

    pattern2 = image.crop(t_coords)
    pattern2.save('t.png')

    pattern3 = image.crop(e_coords)
    pattern3.save('e.png')

    pattern4 = image.crop(x_coords)
    pattern4.save('x.png')


def get_pattern_image(source):
    image = get_image(source)
    pattern = image.crop(pattern_coords)
    pattern.save('pattern.png')


def get_patterns_columns(data_coords, array_image):
    data = get_data(*data_coords, array_image=array_image)
    patterns = []
    for j in range(len(data[0])):
        column = []
        for i in range(len(data)):
            column.append(data[i][j])
        patterns.append(column)
    return patterns
