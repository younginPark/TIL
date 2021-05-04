from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

prev_page = 0
next_page = (prev_page + 1) + 3
page_cnt = 0

@bp.route('/')
def index():
    global prev_page, next_page
    page_cnt = pagination()
    db, conn = get_db()
    page_num = request.args.get('page_num') # 요구페이지
    if page_num is not None:
        page_num = int(page_num)
        if page_num == -1: # 이전 눌렀을 때
            if prev_page > 0: # 0보다 큰 상태이므로 이전 페이지 빼 줘야 함
                next_page = prev_page+1
                prev_page -= 3
                page_num = prev_page+1
        elif page_num == -999: # 다음 눌렀을 때
            if next_page + 3 <= page_cnt: # 다음 페이지 +3 해도 마지막 페이지 수보다 같거나 작을 때
                prev_page = next_page - 1
                next_page += 3
                page_num = prev_page+1
            elif next_page + 3 > page_cnt: # 다음 페이지 +3 하면 마지막 페이지 수보다 작을 때
                prev_page = next_page - 1
                next_page = page_cnt+1
                page_num = prev_page+1

        db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM posts p JOIN users u ON p.author_id = u.id'
            ' ORDER BY created DESC'
            ' LIMIT 5'
            ' OFFSET %s',
            ((page_num-1)*5,)
        )
        posts = db.fetchall()
        page_num = None
    else:
        prev_page = 0
        if prev_page + 3 > page_cnt:
            next_page = page_cnt
        else:
            next_page = (prev_page + 1) + 3
        db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM posts p JOIN users u ON p.author_id = u.id'
            ' ORDER BY created DESC'
            ' LIMIT 5'
        )
        posts = db.fetchall()
    return render_template('blog/index.html', posts=posts, page_cnt=page_cnt, page_start=prev_page+1, page_last=next_page, page_now=page_num)

def pagination():
    global page_cnt
    db, conn = get_db()
    db.execute(
        'SELECT COUNT(*) FROM posts;'
    )
    post_cnt = db.fetchone() # [8] DictRow
    post_cnt = int(post_cnt['count'])

    # 총 페이지 수 구하기
    if post_cnt % 5 == 0:
        page_cnt = post_cnt // 5
    else:
        page_cnt = (post_cnt // 5) + 1
    
    return page_cnt


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db, conn = get_db()
            db.execute(
                'INSERT INTO posts (title, body, author_id)'
                ' VALUES (%s, %s, %s)',
                (title, body, g.user['id'])
            )
            conn.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    db, conn = get_db()
    db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM posts p JOIN users u ON p.author_id = u.id'
        ' WHERE p.id = %s',
        (id,)
    )
    post = db.fetchone()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db, conn = get_db()
            db.execute(
                'UPDATE posts SET title = %s, body = %s'
                'WHERE id = %s',
                (title, body, id)
            )
            conn.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db, conn = get_db()
    db.execute('DELETE FROM posts WHERE id = %s', (id,))
    conn.commit()
    return redirect(url_for('blog.index'))

@bp.route('/search', methods=('POST',))
def search():
    search_text = request.form.get('search_text')
    db, conn = get_db()
    query = "SELECT p.id, title, body, created, author_id, username\
            FROM posts p JOIN users u ON p.author_id = u.id\
            WHERE title LIKE %s OR body LIKE %s"
    db.execute(query, ('%' + search_text + '%', '%' + search_text + '%'),)
    posts = db.fetchall()
    return render_template('blog/search.html', posts=posts, search_text=search_text)