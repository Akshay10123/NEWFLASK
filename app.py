from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

class ProductInfoForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    version = StringField('Version', validators=[DataRequired()])
    launch_date = DateField('Launch Date', format='%Y-%m-%d', validators=[DataRequired()])
    retirement_date = DateField('Retirement Date', format='%Y-%m-%d', validators=[DataRequired()])
    decision_making = FloatField('Decision Making', default=0)
    monetization = FloatField('Monetization', default=0)
    time_savings = FloatField('Time Savings', default=0)
    reporting = FloatField('Reporting', default=0)
    processes = FloatField('Processes', default=0)
    collaboration = FloatField('Collaboration', default=0)
    documentation_audits = FloatField('Documentation Audits', default=0)
    next = SubmitField('Next')

@app.route('/', methods=['GET', 'POST'])
def step1():
    form = ProductInfoForm()
    if form.validate_on_submit():
        # Store data in session
        session['product_name'] = form.product_name.data
        session['version'] = form.version.data
        session['launch_date'] = form.launch_date.data
        session['retirement_date'] = form.retirement_date.data
        session['decision_making'] = form.decision_making.data
        session['monetization'] = form.monetization.data
        session['time_savings'] = form.time_savings.data
        session['reporting'] = form.reporting.data
        session['processes'] = form.processes.data
        session['collaboration'] = form.collaboration.data
        session['documentation_audits'] = form.documentation_audits.data

        return redirect(url_for('step2'))  # Redirect to step 2

    return render_template('step1.html', form=form)

# @app.route('/step2', methods=['GET', 'POST'])
# def step2():
#     if request.method == 'POST':
#         # Collect data for multiple product owners
#         num_owners = int(request.form.get('num_owners', 1))  # Default to 1 if not set
#         product_owners = []

#         for i in range(num_owners):
#             owner_data = {
#                 'name': request.form.get(f'product_owner_name_{i}'),
#                 'zid': request.form.get(f'product_owner_zid_{i}'),
#                 'email': request.form.get(f'product_owner_email_{i}'),
#                 'type': request.form.get(f'product_owner_type_{i}'),
#                 'valid_from': request.form.get(f'valid_from_date_{i}')
#             }
#             product_owners.append(owner_data)
        
#         # Store product owners in the session
#         session['product_owners'] = product_owners
        
#         # Redirect to step 3
#         return redirect(url_for('step3'))  

#     # Render form for product owner input without passing a form instance
#     return render_template('step2.html', num_owners=1)

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if request.method == 'POST':
        # Collect data for multiple product owners
        num_owners = int(request.form.get('num_owners', 1))  # Default to 1 if not set
        product_owners = []

        for i in range(num_owners):
            owner_data = {
                'name': request.form.get(f'product_owner_name_{i}'),
                'zid': request.form.get(f'product_owner_zid_{i}'),
                'email': request.form.get(f'product_owner_email_{i}'),
                'type': request.form.get(f'product_owner_type_{i}'),
                'valid_from': request.form.get(f'valid_from_date_{i}')
            }
            product_owners.append(owner_data)
        
        # Store product owners in the session
        session['product_owners'] = product_owners  # Ensure this stores all owners correctly
        
        # Redirect to step 3
        return redirect(url_for('step3'))  

    # Render form for product owner input without passing a form instance
    return render_template('step2.html', num_owners=1)


@app.route('/step3', methods=['GET', 'POST'])
def step3():
    if request.method == 'POST':
        # Handle the logic for Nucleus data
        session['nucleus_data'] = request.form.get('nucleus_data')
        return redirect(url_for('step4'))  # Redirect to step 4

    return render_template('step3.html')

@app.route('/step4', methods=['GET', 'POST'])
def step4():
    if request.method == 'POST':
        # Handle the logic for other data
        session['other_data'] = request.form.get('other_data')
        return redirect(url_for('step5'))  # Redirect to step 5

    return render_template('step4.html')

@app.route('/step5', methods=['GET', 'POST'])
def step5():
    if request.method == 'POST':
        # Handle the logic for platform technologies
        session['platform_name'] = request.form.get('platform_name')
        session['platform_version'] = request.form.get('platform_version')
        return redirect(url_for('review'))  # Redirect to review page

    return render_template('step5.html')

@app.route('/review', methods=['GET'])
def review():
    # Display the review of all data collected
    return render_template('review.html', data=session)

if __name__ == '__main__':
    app.run(debug=True)
