# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import flash, redirect, url_for, render_template, request

from sayhello import app, db
from sayhello.forms import HelloForm
from sayhello.models import Message


@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('提交成功!')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    messages = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', form=form, messages=messages.items, pagination=messages)


    # messages = Message.query.order_by(Message.timestamp.desc()).all()
    # return render_template('index.html', form=form, messages=messages)


@app.route('/manage_messages', methods=['GET', 'POST'])
def manage_messages():
    # 获取当前页码
    page = request.args.get('page', 1, type=int)
    # 每页显示的消息数量
    per_page = 10
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=per_page)
    messages = pagination.items

    if request.method == 'POST':
        # 批量删除
        delete_ids = request.form.getlist('delete_ids')
        if delete_ids:
            Message.query.filter(Message.id.in_(delete_ids)).delete(synchronize_session=False)
            db.session.commit()
            flash('选中的消息已删除!', 'success')

        # 单个编辑
        edit_id = request.form.get('edit_id')
        new_body = request.form.get('new_body')
        if edit_id and new_body:
            message_to_edit = Message.query.get(edit_id)
            if message_to_edit:
                message_to_edit.body = new_body
                db.session.commit()
                flash('消息已更新!', 'success')

        return redirect(url_for('manage_messages', page=page))

    return render_template('manage_messages.html', messages=messages, pagination=pagination)