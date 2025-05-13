from flask import Blueprint, render_template

statistics = Blueprint(
    'statistics',
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='/statistics/static',
)

@statistics.route('/statistics')
def statistics_page():
    return render_template('statistics.html')