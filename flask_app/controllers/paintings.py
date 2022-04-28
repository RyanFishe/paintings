from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models import user, painting


@app.route('/painting/create', methods=["POST"])
def create_painting():
    # Checks if the cook time was inputted
    option = request.form.get('quantity')
    if not painting.Painting.validate_painting(request.form):
        return redirect('/painting/add')

    data = {
        "name":request.form['name'],
        "artist": session['full_name'],
        "description": request.form['description'],
        "price":request.form['price'],
        "quantity": request.form['quantity'],
        "user_id": request.form['user_id']
    }

    painting.Painting.save(data)
    return redirect('/dashboard');

@app.route('/painting/add')
def show_add_page():
    return render_template('add_painting.html')
        

@app.route('/edit_painting', methods=["POST"])
def edit_painting():
    # Checks if the cook time was inputted

    if not painting.Painting.validate_painting(request.form):
        return redirect(request.referrer)
    data = {
        
        "name":request.form['name'],
        "artist": session['full_name'],
        "description": request.form['description'],
        "price":request.form['price'],
        "quantity": request.form['quantity'],
        "user_id": request.form['user_id'],
        "id":request.form['id']
    }

    painting.Painting.update(data)
    return redirect('/dashboard');

@app.route('/painting/<int:id>')
def show_painting(id):
    if 'user_id' not in session:
        flash('Not logged in!')
        return render_template('/index.html')
    data = {
        "id": id
    }
    return render_template('view_painting.html', painting=painting.Painting.get_one(data))

@app.route('/painting/edit/<int:id>')
def show_edit_painting(id):
    if 'user_id' not in session:
        flash('Not logged in!')
        return render_template('/index.html')
    data = {
        "id": id
    }
    return render_template('edit_painting.html', painting=painting.Painting.get_one(data))


@app.route('/delete/<int:id>')
def delete_painting(id):
    painting.Painting.delete(id)
    return redirect('/dashboard')
