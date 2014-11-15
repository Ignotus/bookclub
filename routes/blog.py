from include import *


@app.route('/blog')
def blog():
    return render_template('blog.html')