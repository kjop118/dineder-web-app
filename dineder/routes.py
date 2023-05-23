import secrets

from flask import render_template, url_for, flash, redirect, request, session
from dineder import app, db, bcrypt, search
from dineder.forms import RegistrationForm, LoginForm #, UpdateAccountForm, ProductForm, PostForm
from dineder.models import Users
from flask_login import login_user, current_user, logout_user, login_required
import stripe

# publishable_key = 'pk_test_51LDow7HzCBPomSPtpCIraRVdErr2zpLEvGYGortt1js5KKNKDFRj8tCWABvxSMLwQxIlrIV5yjwZ2ifGRGnVkOJi00uFhGj9wV'
# stripe.api_key = 'sk_test_51LDow7HzCBPomSPtAA4N5ZiPfZRwQ5s2XwUj1HenYNNUNs0nGtXa3cYZ0xQCXKz8AtECpkZ8kjUjvwgfg43WyFPs00H9UQhNDE'
#
@app.route("/")
@app.route("/home")
def home():
    # posts = Post.query.all();
    return render_template('home.html')

@app.route("/about")
def about():
    # posts = Post.query.all();
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(name=form.name.data, surname=form.surname.data, email=form.email.data, password=hashed_password)
        print(user)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        # flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# @app.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():
#     customer_id = current_user.id
#     customer = User.query.filter_by(id=customer_id).first()
#     orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc())
#     customer_tickets = CustomerTicket.query.filter_by(customer_id=customer_id).order_by(CustomerTicket.id.desc())
#
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Account has been updated!', 'success')
#         return redirect(url_for('account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#     # image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
#     # return render_template('account.html', title='Account', image_file=image_file)
#     return render_template('account.html', title='Account', form=form, customer=customer, orders=orders, customer_tickets=customer_tickets)





# @app.route('/payment', methods = ['POST'])
# @login_required
# def payment():
#     invoice = request.form.get('invoice')
#     amount = request.form.get('amount')
#     print(amount)
#
#     customer = stripe.Customer.create(
#         email = request.form['stripeEmail'],
#         source = 'tok_visa'
#     )
#
#     charge = stripe.Charge.create(
#         customer = customer.id,
#         description = 'Ski Geek',
#         amount = amount,
#         currency = 'pln'
#     )
#
#     orders = CustomerOrder.query.filter_by(customer_id=current_user.id).order_by(CustomerOrder.id.desc()).first()
#     orders.status = 'Paid'
#     db.session.commit()
#     return redirect(url_for('thanks'))


# @app.route('/ticketpayment', methods = ['POST'])
# @login_required
# def ticket_payment():
#     invoice = request.form.get('invoice')
#     amount = request.form.get('amount')
#     print(amount)
#
#     customer = stripe.Customer.create(
#         email = request.form['stripeEmail'],
#         source = 'tok_visa'
#     )
#
#     charge = stripe.Charge.create(
#         customer = customer.id,
#         description = 'Ski Geek',
#         amount = amount,
#         currency = 'pln'
#     )
#
#     customer_ticket = CustomerTicket.query.filter_by(invoice=invoice).order_by(CustomerTicket.id.desc()).first()
#     customer_ticket.status = 'Paid'
#     db.session.commit()
#     return redirect(url_for('thanks'))

# @app.route('/ticketpayment', methods = ['POST'])
# @login_required
# def ticket_payment():
#     invoice = request.form.get('invoice')
#     amount = request.form.get('amount')
#     print(amount)
#
#     customer = stripe.Customer.create(
#         email = request.form['stripeEmail'],
#         source = 'tok_visa'
#     )
#
#     charge = stripe.Charge.create(
#         customer = customer.id,
#         description = 'Ski Geek',
#         amount = amount,
#         currency = 'pln'
#     )
#
#     customer_ticket = CustomerTicket.query.filter_by(invoice=invoice).order_by(CustomerTicket.id.desc()).first()
#     customer_ticket.status = 'Paid'
#     db.session.commit()
#     return redirect(url_for('thanks'))


#
# @app.route('/thanks')
# def thanks():
#     return render_template('thank.html')



#
# # @app.route("/about")
# # def about():
# #     return render_template('about.html', title='About')
#
# # @app.route("/offer")
# # def offer():
# #     return render_template('offer.html', title='Offer')
#
#

#
# @app.route("/offer")
# def getProduct():
#     page = request.args.get('page', 1, type=int)
#     # products = Addproduct.query.filter(Addproduct.stock > 0)
#     rows = Product.query.filter(Product.quantity > 0).order_by(Product.id.desc()).paginate(page=page, per_page=4)
#     # brands = Brand.querry.all()
#     return render_template('offer.html', title='Offer',products=rows)
#
# @app.route('/product/<int:id>')
# def single_page(id):
#     product = Product.query.get_or_404(id)
#     return render_template('single_page.html', product=product)
#
# @app.route("/search", methods=['GET','POST'])
# @login_required
# def search():
#     return True
#
# @app.route("/addcart", methods=['POST'])
# def AddCart():
#     # form = ProductForm()
#     # product = Product.query.filter_by(id=1).first()
#     # size = product.size.split(',')
#     # print(size[0])
#     # if current_user.is_authenticated:
#         try:
#             product_id = request.form.get('product_id')
#             quantity = int(request.form.get('quantity'))
#             size = request.form.get('size')
#             product = Product.query.(id=product_id).first()
#
#             if product_id and quantity and size and request.method == "POST":
#                 DictItems = {product_id:{'name':product.name, 'price':float(product.price),
#                                            'category':product.category, 'quantity':int(quantity), 'image':product.image, 'size':size, 'sizes':product.size}}
#                 print(product.size)
#                 if 'Shoppingcart' in session:
#                     # print(session['Shoppingcart'])
#                     if product_id in session['Shoppingcart']:
#                         for key, item in session['Shoppingcart'].items():
#                             if int(key) == int(product_id):
#                                 if item['size'] == size:
#                                     print("ten sam rozmiar")
#                                     session.modified = True
#                                     item['quantity'] += 1
#                                     if(product.quantity>0):
#                                         product.quantity -= quantity;
#                                         db.session.commit()
#                                 else:
#                                     product.quantity += int(item['quantity'])
#                                     product.quantity -= quantity;
#                                     db.session.commit()
#
#                                     session['Shoppingcart'] = DictItems
#                         # print("This product is already in your cart")
#                     else:
#                         session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems )
#                         if (product.quantity > 0):
#                             product.quantity -= quantity;
#                             db.session.commit()
#                         return redirect(request.referrer)
#                 else:
#                     session['Shoppingcart'] = DictItems
#                     if (product.quantity > 0):
#                         product.quantity -= quantity;
#                         db.session.commit()
#                     return redirect(request.referrer)
#         except Exception as e:
#             print(e)
#         finally:
#             return redirect(request.referrer)
#     # else:
#     #     return redirect(request.base_url)
#
#
# def MergeDicts(dict1, dict2):
#     if isinstance(dict1, list) and isinstance(dict2, list):
#         return dict1 + dict2
#     elif isinstance(dict1, dict) and isinstance(dict2, dict):
#         return dict(list(dict1.items()) + list(dict2.items()))
#     return False
#
# @app.route('/cart')
# def getCart():
#     form = ProductForm()
#     if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
#         return redirect(url_for('getProduct'))
#     subtotal = 0
#     randtotal = 0
#     items = Product.query.all()
#     for key, product in session['Shoppingcart'].items():
#         subtotal += float(product['price']) * int(product['quantity'])
#         # tax = ("%.2f" % (.23 * float(subtotal)))
#         # grandtotal = float("%.2f" % (1.23 * subtotal))
#         grandtotal = float(subtotal)
#     return render_template('carts.html', title='Cart',grandtotal=grandtotal, items=items)
#     # , form=form)
#
#
# @app.route('/result')
# def result():
#     searchword = request.args.get('q')
#     products = Product.query.msearch(searchword, fields=['name','description'])
#     return render_template('result.html',products=products)
#
#
# #
# # @app.route('/search', methods=['GET', 'POST'])
# # def index():
# #     search = MusicSearchForm(request.form)
# #     if request.method == 'POST':
# #         return search_results(search)
# #     return render_template('index.html', form=search)
#
# @app.route('/updatecart/<int:code>', methods=['POST'])
# def updatecart(code):
#
#     if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
#         return redirect(url_for('getProduct'))
#     if request.method == "POST":
#         quantity = request.form.get('quantity')
#         size = request.form.get('size')
#
#
#         try:
#             session.modified = True
#
#             for key, item in session['Shoppingcart'].items():
#                 if int(key) == code:
#                     product = Product.query.get(code)
#                     product.quantity += int(item['quantity'])
#                     product.quantity -= int(quantity)
#                     db.session.commit()
#                     item['quantity'] = quantity
#                     item['size'] = size
#                     flash('Item updated', 'success')
#                     return redirect(url_for('getCart'))
#         except Exception as e:
#             print(e)
#             return redirect(url_for('getCart'))
#
# @app.route('/deleteitem/<int:id>')
# def deleteitem(id):
#     if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
#         return redirect(url_for('getProduct'))
#     try:
#         session.modified = True
#         for key , item in session['Shoppingcart'].items():
#             if int(key) == id:
#                 product = Product.query.get(id)
#                 product.quantity += int(item['quantity'])
#                 db.session.commit()
#
#                 session['Shoppingcart'].pop(key, None)
#                 return redirect(url_for('getCart'))
#     except Exception as e:
#         print(e)
#         return redirect(url_for('getCart'))
#
#
# @app.route('/clearcart')
# def clearcart():
#     if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
#         return redirect(url_for('getProduct'))
#
#     try:
#         session.modified = True
#         for key, item in session['Shoppingcart'].items():
#             product = Product.query.get(key)
#             product.quantity += int(item['quantity'])
#             db.session.commit()
#
#         session.pop('Shoppingcart', None)
#         return redirect(url_for('getCart'))
#     except Exception as e:
#         print(e)
#
# def updateshoppingcart():
#     for key, product in session['Shoppingcart'].items():
#         session.modified = True
#         del product['image']
#
#     return updateshoppingcart
#
#
# @app.route('/getorder')
# @login_required
# def get_order():
#     if current_user.is_authenticated:
#         customer_id = current_user.id
#         invoice = secrets.token_hex(5)
#         grandtotal = 0
#         subtotal = 0
#         for order in session['Shoppingcart'].items():
#             subtotal = order[1]['price'] * float(order[1]['quantity'])
#             grandtotal += subtotal
#         print(grandtotal)
#
#         updateshoppingcart()
#
#         try:
#             order = CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'], grandtotal=grandtotal)
#             db.session.add(order)
#             db.session.commit()
#
#
#             session.pop('Shoppingcart')
#             # flash('You order has been sent', 'success')
#             return redirect(url_for('orders', invoice=invoice))
#
#         except Exception as e:
#             print(e)
#             flash('Problem with order', 'danger')
#             return redirect(url_for('getCart'))
#
# @app.route('/orders/<invoice>')
# @login_required
# def orders(invoice):
#     if current_user.is_authenticated:
#         grandtotal = 0
#         subtotal = 0
#         customer_id = current_user.id
#         customer = Users.query.filter_by(id=customer_id).first()
#         orders = CustomerOrder.query.filter_by(invoice=invoice).order_by(CustomerOrder.id.desc()).first()
#
#         for _key, product in orders.orders.items():
#             subtotal += float(product['price']) * int(product['quantity'])
#             grandtotal = ("%.2f" % float(subtotal))
#     else:
#         return redirect(url_for('login'))
#     return render_template('orders.html', invoice=invoice, subtotal=subtotal, grandtotal=grandtotal, customer=customer, orders=orders)
#
# @app.route("/comment/new", methods=['GET', 'POST'])
# @login_required
# def new_post():
#     form = PostForm()
#
#     if form.validate_on_submit():
#         post = Post(title=form.title.data, content=form.content.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('Your post has been create', 'success')
#         return redirect(url_for('home'))
#     return render_template('post.html', form=form, legend='New comment')
#
#
# @app.route("/comment/update/<int:post_id>", methods=['GET', 'POST'])
# @login_required
# def updatePost(post_id):
#     post = Post.query.get_or_404(post_id)
#     form = PostForm()
#
#     if form.validate_on_submit():
#         print("w srodku")
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated', 'success')
#         return redirect(url_for('updatePost', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#
#     return render_template('update_post.html', form=form, post=post, legend='Edit comment')
#
#
# @app.route("/comment/delete/<int:post_id>", methods=['GET', 'POST'])
# @login_required
# def deletePost(post_id):
#     post = Post.query.get_or_404(post_id)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted', 'success')
#     return redirect(url_for('home'))
#
#
# @app.route("/ticket")
# # @login_required
# def ticket():
#     tickets = Ticket.query.all()
#     return render_template('ticket.html', tickets = tickets)
#
#
#
# @app.route('/getticket/<int:ticket_id>', methods=['POST','GET'])
# @login_required
# def get_ticket(ticket_id):
#     if current_user.is_authenticated:
#         customer_id = current_user.id
#         invoice = secrets.token_hex(5)
#
#         if request.method == "POST":
#             quantity = int(request.form.get('quantity'))
#             ticket = Ticket.query.get(ticket_id)
#         # print(ticket)
#             price = float(ticket.price)
#             print(price)
#             print(quantity)
#             subtotal = float(quantity*price)
#             print(subtotal)
#
#             try:
#                 customer_ticket = CustomerTicket(invoice=invoice,customer_id=customer_id,ski_pass=ticket.ski_pass, type=ticket.type,
#                                        amount=ticket.amount, price=ticket.price, quantity=quantity, grandtotal=subtotal)
#                 db.session.add(customer_ticket)
#                 db.session.commit()
#                 flash('Tickets ordered', 'success')
#                 return redirect(url_for('ticket_orders', invoice=invoice))
#
#             except Exception as e:
#                 print(e)
#                 flash('Problem with order', 'danger')
#                 return redirect(url_for('ticket'))
#
#     return redirect(url_for('ticket'))
#
#
# @app.route('/ticketorders/<invoice>')
# @login_required
# def ticket_orders(invoice):
#     if current_user.is_authenticated:
#         grandtotal = 0
#         subtotal = 0
#         customer_id = current_user.id
#         customer = Users.query.filter_by(id=customer_id).first()
#         customer_ticket = CustomerTicket.query.filter_by(invoice=invoice).order_by(CustomerTicket.id.desc()).first()
#         subtotal = customer_ticket.grandtotal
#         grandtotal = subtotal
#
#     else:
#         return redirect(url_for('ticket'))
#     return render_template('ticketOrders.html', invoice=invoice, grandtotal=grandtotal, customer=customer, customer_ticket=customer_ticket)
#
#
#
# @app.route('/returnorder/<invoice>')
# @login_required
# def return_order(invoice):
#     if current_user.is_authenticated:
#         grandtotal = 0
#         subtotal = 0
#         customer_id = current_user.id
#         customer = Users.query.filter_by(id=customer_id).first()
#         orders = CustomerOrder.query.filter_by(invoice=invoice).order_by(CustomerOrder.id.desc()).first()
#
#         for _key, product in orders.orders.items():
#             quantity = product['quantity']
#             p = Product.query.get(_key)
#             p.quantity += quantity
#             db.session.commit()
#
#         db.session.delete(orders)
#         db.session.commit()
#         flash('Order Returned', 'success')
#     else:
#         return redirect(url_for('home'))
#     return redirect(url_for('home'))
#     # return render_template('orders.html', invoice=invoice, subtotal=subtotal, grandtotal=grandtotal, customer=customer, orders=orders)
