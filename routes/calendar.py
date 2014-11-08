from include import *


@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')
