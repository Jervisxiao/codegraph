from flask import render_template, Flask, jsonify, request, redirect
from app import app, code_tree_view



@app.route('/index')
def index():   
    return render_template('tree.html')  

@app.route('/')
@app.route('/about')
def about():   
    return render_template('about.html')  
    

@app.route('/gettree',methods=['GET', 'POST'])      
def get_tree():
    tree = code_tree_view.GetTree()
    result=[]
    url = request.get_data()
    print(type(url))
    #url='https://raw.githubusercontent.com/ZiyeHan/pseudo-py-codes/master/pseudo-py-1.py'
    if url != '':
        print(url)
        code_in_str_list = tree.read_code(url)
        level_list, function_list = tree.get_level_name(code_in_str_list)
        class_list = tree.get_class(function_list)
        family = tree.layout_code(level_list, function_list,class_list)
        code_content = tree.print_code(url)
        result.append(family)
        result.append(code_content)
        return jsonify(result)
    else: 
        return jsonify({})

    
