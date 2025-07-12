from flask import Flask,render_template,request,redirect,url_for,flash,session
from backend.users import is_registered,verify_user,add_user

# [X] Invalid quantity value in DB: 


app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login/username', methods=['POST'])
def login_username():
    username = request.form['username']
    password = request.form['password']

    if not is_registered(username=username):
        flash("User not found.")
        return redirect(url_for('login'))

    user = verify_user(username=username, input_password=password)
    if not user:
        flash("Incorrect password.")
        return redirect(url_for('login'))

    session['user'] = user[0]  # assuming user[0] = username or ID
    flash("Logged in successfully!")
    return redirect(url_for('dashboard'))

@app.route('/login/email', methods=['POST'])
def login_email():
    email = request.form['email']
    password = request.form['password']

    if not is_registered(email=email):
        flash("User not found.")
        return redirect(url_for('login'))

    user = verify_user(email=email, input_password=password)
    if not user:
        flash("Incorrect password.")
        return redirect(url_for('login'))

    session['user'] = user[0]
    flash("Logged in successfully!")
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash("Passwords do not match.")
            return redirect(url_for('register'))

        if is_registered(username=username) or is_registered(email=email):
            flash("Username or email already exists.")
            return redirect(url_for('register'))

        add_user(username, fname, lname, email, password)
        flash("Account created successfully! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        flash("Please log in to access the dashboard.")
        return redirect(url_for('login'))

    # Totals and counts
    import backend.raw_materials as raw
    import backend.semi_finished as semi
    import backend.finished as finished
    import backend.sales_orders as so
    
    raw_count = raw.get_count_raw()
    semi_count = semi.get_count_semi()
    finished_count = finished.get_count_finished()
    orders_count = so.get_count_sales_order()
    recent_orders = so.get_recent_orders()

    return render_template("dashboard.html",
                            raw_count=raw_count,
                            semi_count=semi_count,
                            finished_count=finished_count,
                            orders_count  = orders_count,
                            order_count=recent_orders,
                            active_page='inventory')



@app.route('/products', methods=['GET', 'POST'])
def inventory():
    if 'user' not in session:
        flash("Please log in to access the dashboard.")
        return redirect(url_for('login'))

    import backend.raw_materials as raw
    import backend.semi_finished as semi
    import backend.finished as finished
    import backend.sales_orders as sales
    
    if request.method == 'POST':
        action = request.form.get("action")
        item_type = request.form.get('type')
        prod_id_raw = request.form.get('prod_id', "0")

        try:
            item_id = int(prod_id_raw)
        except (ValueError, TypeError):
            item_id = None

        name = request.form.get("name", "").strip().title()
        category = request.form.get("category", "").strip()
        price_raw = request.form.get("price")
        quantity_raw = request.form.get("quantity")

        price = float(price_raw) if price_raw else None
        quantity = float(quantity_raw) if quantity_raw else None


        if action == 'add':
            if not name.isalpha() or not category.isalpha():
                flash("Name and Category must only contain letters.")
                return redirect(url_for('inventory'))
            
            if item_type == 'raw':
                raw.add_raw(name, category, price, quantity)
            elif item_type == 'semi':
                semi.add_semi(name, category, price, quantity)
            elif item_type == 'finished':
                finished.add_finished(name, category, price, quantity)

        elif action == 'edit' and item_id:
            if item_type == 'raw':
                raw.edit_raw(
                    item_id,
                    name=name if name else None,
                    category=category if category else None,
                    price=price if request.form.get("price") else None,
                    quantity=quantity if request.form.get("quantity") else None
                )
            elif item_type == 'semi':
                semi.edit_semi(
                    item_id,
                    name=name if name else None,
                    category=category if category else None,
                    price=price if request.form.get("price") else None,
                    quantity=quantity if request.form.get("quantity") else None
                )
            elif item_type == 'finished':
                finished.edit_finished(
                    item_id,
                    name=name if name else None,
                    category=category if category else None,
                    price=price if request.form.get("price") else None,
                    quantity=quantity if request.form.get("quantity") else None
                )

        elif action == 'delete' and item_id:
            if item_type == 'raw':
                raw.delete_raw_id(item_id)
            elif item_type == 'semi':
                semi.delete_semi(item_id)
            elif item_type == 'finished':
                finished.delete_finished(item_id)

        return redirect(url_for('inventory'))

    inventory_raw = raw.view_raw()
    semi_finished_data = semi.view_semi()
    finished_products_data = finished.view_finished()

    raw_count = len(inventory_raw)
    semi_count = len(semi_finished_data)
    finished_count = len(finished_products_data)
    orders_count = sales.get_count_sales_order()

    return render_template("products.html",
                           inventory=inventory_raw,
                           semi_finished=semi_finished_data,
                           finished_products=finished_products_data,
                           raw_count=raw_count,
                           semi_count=semi_count,
                           finished_count=finished_count,
                           orders_count=orders_count,
                           active_page="products")


@app.route('/bom', methods=['GET', 'POST'])
def bom():
    import backend.raw_materials as raw
    import backend.semi_finished as semi
    import backend.finished as finished
    import backend.sales_orders as sales
    from backend.bom import add_bom_components, get_all_boms, get_bom, update_bom_component, delete_bom_component,delete_bom, check_bom_completeness
    selected_product = {}
    message = ""
    selected_bom = None
    completeness = None

    if request.method == "POST":
        action = request.form.get("action")
        prod_name = request.form.get("prod_name")

        prod_name = prod_name.title() if prod_name else ""
        comp_name = request.form.get("comp_name")
        quantity = request.form.get("qty")

        if action == "add":
            success, msg = add_bom_components(prod_name, comp_name, quantity)
        elif action == "update":
            success, msg = update_bom_component(prod_name, comp_name, quantity)
        elif action == "delete":
            success, msg = delete_bom_component(prod_name, comp_name)
        elif action == "delete_bom":
            success, msg = delete_bom(prod_name)
            selected_bom = {}
            selected_product = prod_name.title() if prod_name else ""
            msg = "[✔] BOM check complete"
        elif action == "check":
            _, completeness = check_bom_completeness(prod_name)
            selected_bom = completeness
            selected_product = prod_name.title() if prod_name else ""
            msg = "[✔] BOM check complete" 
        else:
            success, msg = False, "[X] Unknown action"
        
        message = msg
        if action not in ["check", "delete_bom"]:
            success, selected_bom = get_bom(prod_name)
            selected_product = prod_name.title() if prod_name else ""
    success, boms = get_all_boms()
    if not success:
        boms = {}

    inventory_raw = raw.view_raw()
    semi_finished_data = semi.view_semi()
    finished_products_data = finished.view_finished()

    raw_count = len(inventory_raw)
    semi_count = len(semi_finished_data)
    finished_count = len(finished_products_data)
    orders_count = sales.get_all_orders()
    orders_count = sales.get_count_sales_order()

    return render_template("bom.html",
                           inventory=inventory_raw,
                           semi_finished=semi_finished_data,
                           finished_products=finished_products_data,
                           raw_count=raw_count,
                           semi_count=semi_count,
                           finished_count=finished_count,
                           orders_count=orders_count,
                           selected_bom = selected_bom,
                           selected_product = selected_product,
                           boms = boms,
                           completeness = completeness,
                           message = message,
                           active_page="bom")

@app.route("/production", methods=["GET", "POST"])
def production():
    import backend.raw_materials as raw
    import backend.semi_finished as semi
    import backend.finished as finished
    import backend.sales_orders as sales
    from backend.bom import get_all_bom, check_bom_completeness

    message = ""
    selected_product = None
    product_type = None
    max_producible = None
    existing_product = None 

    if request.method == "POST":
        product_type = request.form.get("product_type", "").lower()
        selected_product = request.form.get("product_name", "").title()
        action = request.form.get("action")
        existing_product = finished.search_finished(selected_product)

        price_input = request.form.get("price", "").strip()
        try:
            quantity = float(request.form.get("quantity", 0))
            price = float(price_input) if price_input else None
        except ValueError:
            return "Quantity and price must be numbers.", 400
        
        if not selected_product or product_type not in ["finished", "semi"]:
            message = "[X] Please select a valid product and type."
        else:
            # Check BOM completeness from DB
            complete, report = check_bom_completeness(selected_product)

            if not complete:
                result_lines = [
                    f"{c['component']} → {c['status']} (Req: {c['required']} | Avail: {c['available']})"
                    for c in report
                ]
                message = f"[X] Incomplete BOM for {selected_product}:\n" + "\n".join(result_lines)
            else:
                if action == "produce":
                    if product_type == "finished":
                        success, result = finished.produce_finished(selected_product, quantity, price)
                    else:
                        success, result = semi.produce_semi_finished(selected_product, quantity, price)

                    if success:
                        flash(result, "success")
                        return redirect("/production")
                    else:
                        message = result

                elif action == "check":
                    message = f"[✔] BOM check complete and sufficient for {selected_product}."
    
    inventory_raw = raw.view_raw()
    semi_finished_data = semi.view_semi()
    finished_products_data = finished.view_finished()
    
    bom_detail = get_all_bom()
    all_products = bom_detail
    raw_count = len(inventory_raw)
    semi_count = len(semi_finished_data)
    finished_count = len(finished_products_data)
    orders_count = sales.get_count_sales_order()

    return render_template("production.html",
        is_new_product= not bool(existing_product), 
        inventory_raw=inventory_raw,
        semi_finished=semi_finished_data,
        finished_products=finished_products_data,
        raw_count=raw_count,
        semi_count=semi_count,
        finished_count=finished_count,
        order_count=orders_count,
        all_products=all_products,
        selected_product=selected_product,
        product_type=product_type,
        max_producible=max_producible,
        message=message,
        active_page='production'
    )



if __name__ == '__main__':
  app.run(host = "0.0.0.0", debug=True)
