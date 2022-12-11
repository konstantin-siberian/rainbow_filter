
from flask import Flask, render_template, request,send_file
import numpy as np
import string
import random
from PIL import Image

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_color_DARK(colorRGB1, colorRGB2):
    return [int((colorRGB1[0]+colorRGB2[0])/2),int((colorRGB1[1]+colorRGB2[1])/2),int((colorRGB1[2]+colorRGB2[2])/2)]

def transform(file_contents):
    color_const = file_contents.shape[0] / 6
    ar_colors = [[228, 3, 3], [255, 140, 0], [255, 237, 0], [0, 128, 38], [36, 64, 142], [115, 41, 130], [115, 41, 130]]
    for i in range(file_contents.shape[0]):
        for j in range(file_contents.shape[1]):
            gray_value = int(round(file_contents[i][j][0] * 0.07 + file_contents[i][j][1] * 0.72 + file_contents[i][j][2] * 0.21, 0))

            # data[i][j][:]=get_color_BRIGHT(ar_colors[int(i//color_const)],[gray_value,gray_value,gray_value])
            file_contents[i][j][:] = get_color_DARK(ar_colors[int(i // color_const)], [gray_value, gray_value, gray_value])

            # data[i][j][:]=get_color_DARK(ar_colors[int(i//color_const)],data[i][j])

    im = Image.fromarray(file_contents)
    im_path=id_generator()
    im.save('static/'+im_path+'.png')
    return im_path
    # return im

'''
mimetype='image/png'

TypeError: Unable to detect the MIME type because a file name is not available. Either set 'download_name', pass a path instead of a file, or set 'mimetype'.

'''

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def form():
        return render_template('template1.html')

    @app.route('/transform', methods=["POST"])
    def transform_view():
        request_file = request.files['data_file']
        if not request_file:
            return "No file was submitted"

        im = Image.open(request_file)
        data = np.array(im)

        result = transform(data)
        html_string='''<html>
  <body>
        <link rel="stylesheet" href="/static/css/styles_footer.css"/>
        <img src="/{the_path}" alt="Any image"/>
  </body>
</html>
'''.format(the_path='static/'+result+'.png')
        Html_file = open("templates/success.html", "w")
        Html_file.write(html_string)
        Html_file.close()
        # return send_file('images/'+result+'.png', as_attachment=True,mimetype='image/png')
        return render_template('success.html')

    return app




'''
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)



'''
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)