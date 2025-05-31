from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user,login_required
from app_grocery.form import User_Login,Admin_Login,Signup_User,create_category,create_product,search_field,quantity_order
from flask import render_template, url_for, flash, redirect,request,session
from app_grocery.database import user,Admin,Category,Product,buys
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import func
from app_grocery import app,db,bcrypt
import secrets
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


 
@app.route('/', methods=['GET', 'POST'])
def user_login():
    form = User_Login()
    if form.validate_on_submit():
        names = user.query.filter_by(name=form.username.data).first()
        if names and bcrypt.check_password_hash(names.password, form.password.data):
            login_user(names,remember=form.remember.data)
            flash('Logged In!!','success')
            session['user_id']=names.id
            return redirect(url_for('user_dashboard',user_id=names.id))
        else:
            flash('Username/Password Entered Was Incorrect!','danger')

    return render_template('index.html', title='User Login', form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    form = Admin_Login()
    if form.validate_on_submit():
        names = Admin.query.filter_by(name=form.username.data).first()
        if names and names.password==form.password.data:
            forms=search_field()
            login_user(names)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Username/Password Entered Was Incorrect!','danger')
    return render_template('Admin_Login.html', title='Admin Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Bhai login hein",'success')
    form = Signup_User()
    if form.validate_on_submit():
        passw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = user(name=form.username.data, password=passw, email=form.email.data)
        db.session.add(customer)
        db.session.commit()
        flash(f'Account Successfully Created for {form.username.data}', 'success')
        return redirect(url_for('user_login'))
    return render_template('Signup_User.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('user_login'))
# admin dashboard
@app.route("/admin_dashboard")
def admin_dashboard():
    total_category = Category.query.count()
    total_products = Product.query.count()
    log_datetime = datetime.now()
    date = log_datetime.strftime("%Y-%m-%d")
    time = log_datetime.strftime("%H:%M")
    total_user = user.query.count()
    data = ['Total Users', 'Total Categories', 'Total Products']
    count = [total_user, total_category, total_products]

    plt.bar(data, count)
    plt.xlabel("Total")
    plt.ylabel('Count')

    # Save the plot as an image in the 'static' folder within the 'app_grocery' directory
    chart_filename = 'app_grocery/static/stats.png'
    plt.savefig(chart_filename)

    # Clear the plot to avoid any conflicts
    plt.clf()

    return render_template('Admin_Dashboard.html', title='Admin Dashboard', tc=total_category, tp=total_products,
                           time=time, date=date, to=total_user, forms=session.get('forms'), filename='stats.png')

# create category
@app.route("/create_category",methods=['GET','POST'])
def admin_category():
    form=create_category()
    forms=search_field()
    if form.validate_on_submit():
        category=Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash("Category Added!","success")
        return redirect(url_for('view_category'))
    return render_template('Admin_Category.html',title='Manage Category',form=form,legend='Add Category',forms=forms)

# create product
@app.route("/create_product",methods=['GET','POST'])
def admin_product():
    form=create_product()
    form.initialize()
    forms=search_field()
    if form.validate_on_submit():
        if form.image.data:
            image_name=save_image(form.image.data)
        else:
            image_name='default.jpg'
        product=Product(name=form.name.data,exp_date=form.exp_date.data,price=form.price.data,stock=form.stock.data,image=image_name,category_id=form.category_id.data)
        db.session.add(product)
        db.session.commit()
        flash("Product Added Successfully!","success")
        return redirect(url_for('view_product'))
    filename=url_for('static',filename='product.png')
    return render_template('Admin_Product.html',title='Manage Product',form=form,legend='Add Product',forms=forms,filename=filename)

@app.route("/view_category",methods=['GET','POST'])
def view_category():
    category=Category.query.all()
    forms=search_field()
    return render_template('View_Category.html',title='View Category',categories=category,forms=forms)

@app.route("/view_product",methods=['GET','POST'])
def view_product():
    product= Product.query.all()
    forms=search_field()
    return render_template('View_Product.html',title='View Product',products=product,forms=forms)

@app.route("/category/<int:category_id>/update" ,methods=['GET','POST'])
def update_category(category_id):
    category=Category.query.get_or_404(category_id)
    form=create_category()
    forms=search_field()
    if form.validate_on_submit():
        category.name=form.name.data
        db.session.commit() 
        flash("Category has been Updated Successfully!!" ,"success")
        return redirect(url_for('view_category'))
    elif request.method == 'GET':
        form.name.data=category.name
    return render_template('Admin_Category.html',title='Update Category',form=form,legend='Update Category',forms=forms)


@app.route("/category/<int:category_id>/delete" ,methods=['GET','POST'])
def delete_category(category_id):
    category=Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Category has been Deleted Successfully!!" ,"success")
    return redirect(url_for('view_category'))

@app.route("/category/<int:category_id>/confirm_delete", methods=['GET', 'POST'])
def confirm_delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash("Category has been Deleted Successfully!!", "success")
        return redirect(url_for('view_category'))
    return render_template('confirm_delete_category.html', category=category)


@app.route("/product/<int:product_id>" ,methods=['GET','POST'])
def product(product_id):
    forms=search_field()
    product=Product.query.get_or_404(product_id)
    return render_template('Product.html',title=product.name,product=product,forms=forms)

@app.route("/product/<int:product_id>/update" ,methods=['GET','POST'])
def update_product(product_id):
    product=Product.query.get_or_404(product_id)
    form=create_product()
    form.initialize()
    forms=search_field()
    if form.validate_on_submit():
        if form.image.data:
            image_name=save_image(form.image.data)
            product.image=image_name
        product.name=form.name.data
        product.exp_date=form.exp_date.data
        product.price=form.price.data
        product.stock=form.stock.data
        product.category_id=form.category_id.data
        db.session.commit() 
        flash("Product has been Updated Successfully!!" ,"success")
        return redirect(url_for('view_product'))
    elif request.method == 'GET':
        form.name.data=product.name
        form.exp_date.data=product.exp_date
        form.price.data=product.price
        form.stock.data=product.stock
    filename=url_for('static',filename=product.image)
    return render_template('Admin_Product.html',title='Update Product',form=form,legend='Update Product',forms=forms,filename=filename)

@app.route("/product/<int:product_id>/delete" ,methods=['POST'])
def delete_product(product_id):
    product=Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product has been Deleted Successfully!!" ,"success")
    return redirect(url_for('view_product'))

@app.route("/product/<int:product_id>/confirm_delete", methods=['GET', 'POST'])
def confirm_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash("Product has been Deleted Successfully!!", "success")
        return redirect(url_for('view_product'))
    return render_template('confirm_delete_product.html', product=product)


@app.route("/category/<int:cat_id>/view_by_category",methods=['GET'])
def view_by_category(cat_id):
    forms=search_field()
    products=Product.query.filter_by(category_id=cat_id)
    return render_template("Product.html",title=cat_id,products=products,forms=forms)

@app.route("/user_dashboard/<int:user_id>",methods=['GET','POST'])
@login_required
def user_dashboard(user_id):
    product= Product.query.all()
    forms=search_field()
    return render_template('User_Dashboard.html',title='Dahboard',products=product,user_id=user_id,forms=forms)

@app.route("/orders/<int:user_id>/<int:product_id>", methods=['POST'])
@login_required
def orders(user_id, product_id):
    quantity = int(request.form.get('quantity'))  # Get the quantity from the form data
    if quantity > 0:
        exist_order=db.session.query(buys).filter_by(user_id=user_id, product_id=product_id).first()
        product=Product.query.filter_by(id=product_id).first()
        allowed=product.stock-quantity
        if allowed>=0:
            if exist_order:
                tp=(product.price)*(buys.c.count+quantity)
                product.stock-=quantity
                update_query = buys.update().values(count=buys.c.count + quantity,total_price=tp).where(buys.c.user_id == user_id).where(buys.c.product_id == product_id)
                db.session.execute(update_query)
            else:
                tp=(product.price)*(quantity)
                product.stock-=quantity
                order = buys.insert().values(user_id=user_id, product_id=product_id, count=quantity,total_price=tp)
                db.session.execute(order)
            db.session.commit()
            flash('Item added to cart', 'success')
        else:
            flash('This much quantity is unavailable in stock','danger')
            
    else:
        flash('Invalid quantity', 'danger')
    return redirect(request.referrer)

@app.route("/view_category2",methods=['GET','POST'])
@login_required
def view_category2():
    category=Category.query.all()
    forms=search_field()
    return render_template('User_Category.html',title='View Category',categories=category,user_id=session.get('user_id'),forms=forms)

@app.route("/product2/<int:product_id>" ,methods=['GET','POST'])
@login_required
def product2(product_id):
    product=Product.query.get_or_404(product_id)
    return render_template('User Product.html',title=product.name,product=product,user_id=session.get('user_id'))

@app.route("/category2/<int:cat_id>/view_by_category",methods=['GET'])
@login_required
def view_by_category2(cat_id):
    products=Product.query.filter_by(category_id=cat_id)
    return render_template("User_Product.html",title=cat_id,products=products,user_id=session.get('user_id'))

@app.route('/search',methods=['GET','POST'])
@login_required
def search():
    forms=search_field()
    if forms.validate_on_submit():
        category=Category.query.filter(Category.name.ilike(f'%{forms.search.data}%')).all()
        product=Product.query.filter(Product.name.ilike(f'%{forms.search.data}%')).all()
        if category or product:
            if category:
                return render_template('View_Category.html',title='View Category',categories=category,forms=forms)
            else:
                return render_template('View_Product.html',title='View Product',products=product,forms=forms)
        else:
            flash('No such Categories/Products Found','danger')
    return redirect(url_for('view_category'))

@app.route('/user_search',methods=['GET','POST'])
@login_required
def user_search():
    forms=search_field()
    if forms.validate_on_submit():
        category=Category.query.filter(Category.name.ilike(f'%{forms.search.data}%')).all()
        product=Product.query.filter(Product.name.ilike(f'%{forms.search.data}%')).all()
        if category or product:
            if category:
                return render_template('User_Category.html',title='View Category',categories=category,user_id=session.get('user_id'),forms=forms)
            else:
                return render_template('User_Dashboard.html',title='Dahboard',products=product,user_id=session.get('user_id'),forms=forms)
        else:
            flash('No such Categories/Products Found','danger')
            return redirect(request.referrer)
    return redirect(url_for('cart'))


@app.route('/cart', methods=['GET','POST'])
@login_required
def cart():
    forms = search_field()
    form=quantity_order()
    total_cost=0
    total_quantity=0
    list = db.session.query(buys).filter_by(user_id=session.get('user_id')).all()
    product_ids = [item.product_id for item in list]
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    total_quantity = db.session.query(func.coalesce(func.sum(buys.c.count), 0)).filter_by(user_id=session.get('user_id')).scalar()    
    total_cost=db.session.query(func.coalesce(func.sum(buys.c.total_price),0)).filter_by(user_id=session.get('user_id')).scalar()
    return render_template('User_Cart.html', list=list, user_id=session.get('user_id'), title='Cart', forms=forms, products=products,form=form,tq=total_quantity,tc=total_cost)

@app.route('/delete_cart/<int:user_id>/<int:product_id>',methods=['GET','POST'])
def delete(user_id,product_id):
    product=Product.query.filter_by(id=product_id).first()
    product.stock+=1
    tp=(buys.c.count-1)*product.price
    update_count = buys.update().values(count=buys.c.count-1,total_price=tp).where(buys.c.user_id == user_id).where(buys.c.product_id == product_id)
    db.session.execute(update_count)
    db.session.commit()
    flash("Quantity decreased",'success')
    return redirect(request.referrer)

@app.route('/buy_all',methods=['GET','POST'])
def buy_all():
    db.session.query(buys).filter_by(user_id=session.get('user_id')).delete()
    db.session.commit()
    flash('Your items will be shipped to you soon!!','success')
    return redirect(url_for('cart'))

def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + file_ext
    image_path = os.path.join(app.root_path, 'static', image_filename)
    form_image.save(image_path)
    return image_filename

        
    






    