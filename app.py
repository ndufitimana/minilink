from __future__ import print_function
from crypt import methods
from logging import raiseExceptions
from multiprocessing import connection
from flask import Flask, request, url_for
from flask import render_template, redirect,  flash
from nanoid import generate
import sqlite3

import sys


app = Flask(__name__)
app.config["SECRET_KEY"] = "you will never gess the key" #fix this before deploying
""" This function opens connection to the database that was created
init_db.py """
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods = ['GET', 'POST'])
@app.route("/home")
def index():
    res= False
    link = ""
    if request.method == 'POST':
        try:
            long_link = request.form['long_link']
            if not request.form['alias']:
               alias = generate(size=5)
            elif len(request.form['alias'])>5:
                flash('alias cannot be than 5 characters.')
                return redirect(url_for('index'))
            else:
                alias = request.form['alias']
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute('INSERT INTO links(link_key, content) VALUES(?,?)',
            (alias, long_link))
            res= True
            link = "127.0.0.1:5000/"+alias
            conn.commit()
        except:
            conn.rollback()
            return redirect((url_for('index')))
        conn.close()
    else:
        res = False
    return render_template('index.html', title= "MiniLink", res=res, link=link)

@app.route('/<path:link_id>', methods = ['GET'])
def get_link(link_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        res = cur.execute('SELECT * FROM links WHERE link_key=?', (link_id,)).fetchall()
        long_url = res[0]['content']
        conn.close
        return redirect(long_url) 
        
        
    except:
        conn.rollback()
        return '404 not found'
        
    
    
