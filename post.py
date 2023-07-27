from flask import Blueprint, render_template
import db

# Blueprint インスタンスを作成
# 第1引数は Blueprint の名前
# 第2引数はモジュール名(__name__を指定すればOK)
# 第3引数は Blueprint の URL プレフィックス
book_bp = Blueprint('post', __name__, url_prefix='/post')

# Blueprint インスタンスにルーティングを設定する。
# この場合は book_bp の url_prefix が /book なので
# このメソッドの URL は /book/list となります。
@book_bp.route('/top')
def book_list():
    
    post_list = db.select_all_posts()

    # 返すHTMLは templates フォルダ以降のパスを書きます。
    return render_template('book/top.html', books=post_list)

