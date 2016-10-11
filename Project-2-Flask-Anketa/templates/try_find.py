
@app.route('/result')
def result():
    numsrc = request.args['numsrc']
    namesrc = request.args['namesrc']
    file = open('/Users/macbook/Desktop/HSE void/Flask prog/project_AGAIN/stats.txt', 'r', encoding='UTF-8')
    reader = file.readlines()
    if namesrc != None:
        for line in reader:
            if namesrc in line:
                d = line
    if numsrc != None:
        for line in reader:
            if numsrc in line:
                d = line
            return render_template('result.html', namesrc=namesrc, d=d, numsrc=numsrc)