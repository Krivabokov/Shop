from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/add-product', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        products = Product(name=name, description=description, price=price)

        try:
            db.session.add(products)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка"
    else:
        return render_template("add-product.html")


@app.route('/<int:id>')
def product_detail(id):
    product = Product.query.get(id)
    return render_template("product_detail.html", product=product)


@app.route('/<int:id>/delete')
def product_delete(id):
    product = Product.query.get_or_404(id)

    try:
        db.session.delete(product)
        db.session.commit()
        return redirect('/')
    except:
        return "Ошибка"


@app.route('/<int:id>/update', methods=['POST', 'GET'])
def product_update(id):
    product = Product.query.get(id)
    if request.method == "POST":
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка"
    else:
        return render_template("product_update.html", product=product)


if __name__ == "__main__":
    app.run(debug=True)

with app.app_context():
    db.create_all()
