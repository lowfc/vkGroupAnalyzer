import webbrowser


class Html:
    def __init__(self, scale, filename = 'processed'):
        self.html = str() # html code
        self.filename = filename + '.html' # html file name
        self.script ="""
            window.onload = function() {
            var drawingCanvas = document.getElementById('weights');
            drawingCanvas.width =""" + str(scale+200) +""";
            drawingCanvas.height = """ + str(scale+200) + """;
            if(drawingCanvas && drawingCanvas.getContext) {
            var context = drawingCanvas.getContext('2d');
            context.beginPath();
            context.lineWidth = 5;
            context.strokeStyle = '#5991c3';
            """ # script content
        self.body = "<canvas id='weights'></canvas>\n" # body content
        self.weights = 0
        self.edges = 0
    def _create_skeleton(self): # create first html-skeleton
        self.html = '''
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="unicode" />
            <title>Group Social Graph</title>
            <link rel="shortcut icon" href="./pics/logo.png" type="image/x-icon">
        </head>

        <style>
            html, body
            {
                background-color: #cfe9ff;
            }
            .node
            {
                border-radius: 100px;
                position: absolute;
                width: 100px;
                height: 100px;
                box-shadow: 0 0 5px 2px #7facd3; 
                border: 4px solid #3c709e;
                transition: ease-in .2s;
            }
            .node:hover
            {
                width : 105px;
                height: 105px;
                cursor: pointer;
                transition: ease-in .1s;
                margin-left: -2.5px;
                margin-top: -2.5px;
                box-shadow: 0 0 5px 3px #72affb;
            }
            .info
            {
                margin-top: 120px;
                margin-left: 10px;
            }
            canvas
            {
            left: 0px;
            top: 0px;
            position: absolute; 
            margin: 0;
            padding: 0;
            }
            </style>
    '''
    def __create_file(self):
        html_generator  = open(self.filename,'w',encoding='utf-8')
        html_generator.write(self.html)
        html_generator.close()
    def open_tab(self):
        webbrowser.open_new_tab(self.filename)
    def pack(self):
        self._create_skeleton()
        self.html += '<script>\n' + self.script + '''
        context.closePath();
            context.stroke();
            }
            }
        </script>
        ''' + '<body>\n' + self.body + '''<body><a href="https://vk.com/lowfc" target="new"><img src="../pics/programmer.png"
        class="node" style = "left: 10px; top: 10px;" title="Programmed and designed by lowfc"></a><p class="info">Отрисовано<br>Людей: {peoples}<br>Связей: {friendships}</body>\n'''.format(peoples = self.edges, friendships = self.weights)
        self.__create_file()
    def add_script(self, line): # use for add line to script part (recommend for one-line add)
        self.script += line+'\n'
    def add_body(self, line): # use for add line to body part (recommend for one-line add)
        self.body += line+'\n'
    def add_edge(self, id, x, y, title, img = 'default.jpg'):
        self.body += '<a href="{link}" target="new"><img src="{imger}" class="node" style = "left: {x}px; top: {y}px;" title="{title}"></a>'.format(link = 'https://vk.com/id'+str(id),
        x = x, y = y, title = title, imger = img) + '\n'
        self.edges += 1
    def add_weight(self, x1, y1, x2, y2):
        self.script += 'context.moveTo({x1}, {y1}); \ncontext.lineTo({x2}, {y2});'.format(x1 = x1+50, y1 = y1+50,
        x2 = x2+50, y2 = y2+50)
        self.weights += 1


