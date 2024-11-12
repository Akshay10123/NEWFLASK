from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField
from wtforms.validators import DataRequired
import datetime

app = Flask(__name__)
app.secret_key = 'fsdgdfhfghddffsr'  # Change this to a random secret key

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
    if request.method == 'POST':
        # Product Information
        session['product_name'] = request.form['product_name']
        session['version'] = request.form['version']
        session['launch_date'] = request.form['launch_date']
        session['status'] = request.form['status']
        session['product_properties'] = request.form.getlist('product_properties')
        session['retirement_date'] = request.form['retirement_date']
        session['description'] = request.form['description']
        session['risks'] = request.form['risks']
        session['additional_properties'] = request.form['additional_properties']
        session['documentation_url'] = request.form['documentation_url']
        session['repository_url'] = request.form['repository_url']
        session['metrics_dashboard'] = request.form['metrics_dashboard']

        # Business Value (Slider Value)
        session['decision_making'] = request.form['decision_making']
        session['monetization'] = request.form['monetization']
        session['time_savings'] = request.form['time_savings']
        session['reporting'] = request.form['reporting']
        session['processes'] = request.form['processes']
        session['collaboration'] = request.form['collaboration']
        session['documentation_audits'] = request.form['documentation_audits']        

        # Product Owner Information
        session['product_owner_name'] = request.form['product_owner_name']
        session['product_owner_zid'] = request.form['product_owner_zid']
        session['product_owner_email'] = request.form['product_owner_email']
        session['product_owner_type'] = request.form['product_owner_type']
        session['valid_from_date'] = request.form['valid_from_date']
        session['valid_to_date'] = request.form['valid_to_date']

        return redirect(url_for('step2'))

    today = datetime.date.today().strftime("%Y-%m-%d")
    return render_template('step1.html', today=today)

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if request.method == 'POST':
        # If the "Skip" button was clicked, go directly to Step 3 without saving any data
        if 'skip' in request.form:
            return redirect(url_for('step3'))

        # Collect data for multiple product owners if "Save" button was clicked
        num_owners = int(request.form.get('num_owners', 0))  # Get the number of owners from the form
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
        
        # Store product owners in the session if "Save" is clicked
        session['product_owners'] = product_owners  # Store all owners
        
        # Redirect to Step 3
        return redirect(url_for('step3'))  

    # Render the step2 form with no initial owners
    return render_template('step2.html', num_owners=0)


@app.route('/step3', methods=['GET', 'POST'])
def step3():
    if request.method == 'POST':
        # If the "Skip" button was clicked, go directly to Step 4
        if 'skip' in request.form:
            return redirect(url_for('step4'))

        # Collect data for multiple business owners if "Save" button was clicked
        num_owners = int(request.form.get('num_owners', 0))  # Get the number of owners from the form
        business_owners = []

        for i in range(num_owners):
            owner_data = {
                'name': request.form.get(f'business_contact_name_{i}'),
                'zid': request.form.get(f'business_owner_zid_{i}'),
                'email': request.form.get(f'business_contact_email_{i}'),
                'type': request.form.get(f'business_contact_type_{i}'),
                'valid_from': request.form.get(f'valid_from_date_{i}'),
                'valid_to': request.form.get(f'valid_to_date_{i}')
            }
            business_owners.append(owner_data)
        
        # Store business owners in the session if "Save" is clicked
        session['business_owners'] = business_owners  # Store all owners
        
        # Redirect to Step 4
        return redirect(url_for('step4'))  

    # Render the step3 form
    today = datetime.date.today().strftime("%Y-%m-%d")  # Get today's date in yyyy-mm-dd format
    return render_template('step3.html', today=today)


@app.route('/step4', methods=['GET', 'POST'])
def step4():
    if request.method == 'POST':
        # If the "Skip" button was clicked, go directly to Step 5 without saving any data
        if 'skip' in request.form:
            return redirect(url_for('step5'))

        # Collect data for multiple data sources if "Save" button was clicked
        num_data_sources = int(request.form.get('num_data_sources', 0))  # Get the number of data sources from the form
        data_sources = []

        for i in range(num_data_sources):
            source_data = {
                'database': request.form.get(f'database_name_{i}'),
                'schema': request.form.get(f'schema_name_{i}'),
                'table': request.form.get(f'table_name_{i}'),
                'type': request.form.get(f'snowflake_data_type_{i}'),
                'valid_from': request.form.get(f'valid_from_date_{i}'),
                'valid_to': request.form.get(f'valid_to_date_{i}')
            }
            data_sources.append(source_data)
        
        # Store data sources in the session if "Save" is clicked
        session['data_sources'] = data_sources  # Store all data sources
        
        # Redirect to Step 5
        return redirect(url_for('step5'))  

    # Render the step4 form
    today = datetime.date.today().strftime("%Y-%m-%d")  # Get today's date in yyyy-mm-dd format
    return render_template('step4.html', today=today)


# Route for Step 5: Other Data Sources/Outputs
@app.route('/step5', methods=['GET', 'POST'])
def step5():
    if request.method == 'POST':
        num_data_sources = int(request.form.get('num_data_sources', 0))
        other_data_sources = []
        
        for i in range(num_data_sources):
            other_source_data = {
                'name': request.form.get(f'dataset_name_{i}'),
                'description': request.form.get(f'dataset_description_{i}'),
                'type': request.form.get(f'dataset_type_{i}'),
                'valid_from': request.form.get(f'valid_from_date_{i}'),
                'valid_to': request.form.get(f'valid_to_date_{i}')
            }
            other_data_sources.append(other_source_data)
        
        session['other_data_sources'] = other_data_sources
        return redirect(url_for('step6'))
    
    today = datetime.date.today().strftime("%Y-%m-%d")
    return render_template('step5.html', today=today)

@app.route('/step6', methods=['GET', 'POST'])
def step6():
    if request.method == 'POST':
        # If the "Skip" button was clicked, go directly to the review page without saving any data
        if 'skip' in request.form:
            return redirect(url_for('review'))

        # Collect data for multiple platforms if "Save" button was clicked
        num_platforms = int(request.form.get('num_platforms', 0))  # Get the number of platforms from the form
        platforms = []

        for i in range(num_platforms):
            platform_data = {
                'name': request.form.get(f'platform_name_{i}'),
                'description': request.form.get(f'platform_description_{i}'),
                'valid_from': request.form.get(f'valid_from_date_{i}'),
                'valid_to': request.form.get(f'valid_to_date_{i}')
            }
            platforms.append(platform_data)
        
        # Store platforms in the session if "Save" is clicked
        session['platforms'] = platforms  # Store all platforms
        
        # Redirect to the review page
        return redirect(url_for('review'))  

    # Render the step6 form
    today = datetime.date.today().strftime("%Y-%m-%d")  # Get today's date in yyyy-mm-dd format
    return render_template('step6.html', today=today)


@app.route('/review', methods=['GET', 'POST'])
def review():
    # Gather all collected data from the session
    data = {
        # 'product_name': session.get('product_name'),
        # 'version': session.get('version'),
        # 'launch_date': session.get('launch_date'),
        # 'retirement_date': session.get('retirement_date'),
        # 'decision_making': session.get('decision_making'),
        # 'monetization': session.get('monetization'),
        # 'time_savings': session.get('time_savings'),
        # 'reporting': session.get('reporting'),
        # 'processes': session.get('processes'),
        # 'collaboration': session.get('collaboration'),
        # 'documentation_audits': session.get('documentation_audits'),
        # 'business_owners': session.get('business_owners', []),
        # 'data_sources': session.get('data_sources', []),
        # 'platforms': session.get('platforms', []),
        # 'other_data_sources': session.get('other_data_sources', [])
        # Product Information
        'product_name': session.get('product_name'),
        'version': session.get('version'),
        'launch_date': session.get('launch_date'),
        'status': session.get('status'),
        'product_properties': session.get('product_properties', []),
        'retirement_date': session.get('retirement_date'),
        'description': session.get('description'),
        'product_owner_name': session.get('product_owner_name'),
        'product_owner_zid': session.get('product_owner_zid'),
        'product_owner_email': session.get('product_owner_email'),
        'product_owner_type': session.get('product_owner_type'),
        'valid_from_date': session.get('valid_from_date'),
        'valid_to_date': session.get('valid_to_date'),
        
        # Business Value
        'decision_making': session.get('decision_making'),
        'monetization': session.get('monetization'),
        'time_savings': session.get('time_savings'),
        'reporting': session.get('reporting'),
        'processes': session.get('processes'),
        'collaboration': session.get('collaboration'),
        'documentation_audits': session.get('documentation_audits'),
        
        # Product Description
        'risks': session.get('risks'),
        'additional_properties': session.get('additional_properties'),
        'documentation_url': session.get('documentation_url'),
        'repository_url': session.get('repository_url'),
        'metrics_dashboard': session.get('metrics_dashboard'),

        'product_owners': session.get('product_owners', []),
        'business_owners': session.get('business_owners', []),
        'data_sources': session.get('data_sources', []),
        'platforms': session.get('platforms', []),
        'other_data_sources': session.get('other_data_sources', [])       
        
    }

    # If needed, handle form submission logic here (e.g., final submission)
    if request.method == 'POST':
        # Final submission logic (e.g., save to database, send confirmation)
        # session.clear()  # Optionally clear session after submission
        return redirect(url_for('thank_you'))  # Redirect to a thank you page

    return render_template('review.html', data=data)

@app.route('/submit_final', methods=['POST'])
def submit_final():
    # # Connect to Snowflake
    # conn = get_snowflake_connection()
    # cursor = conn.cursor()

    # try:
    #     # Insert Product Information into Product table
    #     cursor.execute("""
    #         INSERT INTO product_table (product_name, version, launch_date, status, product_properties, retirement_date, description)
    #         VALUES (%s, %s, %s, %s, %s, %s, %s)
    #     """, (
    #         session.get('product_name'),
    #         session.get('version'),
    #         session.get('launch_date'),
    #         session.get('status'),
    #         ', '.join(session.get('product_properties', [])),  # Join the properties as a comma-separated string
    #         session.get('retirement_date'),
    #         session.get('description')
    #     ))

    #     # Insert Business Value data into business_value_table
    #     cursor.execute("""
    #         INSERT INTO business_value_table (decision_making, monetization, time_savings, reporting, processes, collaboration, documentation_audits)
    #         VALUES (%s, %s, %s, %s, %s, %s, %s)
    #     """, (
    #         session.get('decision_making'),
    #         session.get('monetization'),
    #         session.get('time_savings'),
    #         session.get('reporting'),
    #         session.get('processes'),
    #         session.get('collaboration'),
    #         session.get('documentation_audits')
    #     ))

    #     # Insert Product Owner Information into product_owner_table
    #     for owner in session.get('product_owners', []):
    #         cursor.execute("""
    #             INSERT INTO product_owner_table (product_owner_name, product_owner_zid, product_owner_email, product_owner_type, valid_from_date, valid_to_date)
    #             VALUES (%s, %s, %s, %s, %s, %s)
    #         """, (
    #             owner.get('name'),
    #             owner.get('zid'),
    #             owner.get('email'),
    #             owner.get('type'),
    #             owner.get('valid_from'),
    #             owner.get('valid_to')
    #         ))

    #     # Insert Business Owner Information into business_owner_table
    #     for owner in session.get('business_owners', []):
    #         cursor.execute("""
    #             INSERT INTO business_owner_table (business_owner_name, business_owner_zid, business_owner_email, business_owner_type, valid_from_date, valid_to_date)
    #             VALUES (%s, %s, %s, %s, %s, %s)
    #         """, (
    #             owner.get('name'),
    #             owner.get('zid'),
    #             owner.get('email'),
    #             owner.get('type'),
    #             owner.get('valid_from'),
    #             owner.get('valid_to')
    #         ))

    #     # Insert Snowflake Data Sources into snowflake_data_sources_table
    #     for source in session.get('data_sources', []):
    #         cursor.execute("""
    #             INSERT INTO snowflake_data_sources_table (database_name, schema_name, table_name, snowflake_data_type, valid_from_date, valid_to_date)
    #             VALUES (%s, %s, %s, %s, %s, %s)
    #         """, (
    #             source.get('database'),
    #             source.get('schema'),
    #             source.get('table'),
    #             source.get('type'),
    #             source.get('valid_from'),
    #             source.get('valid_to')
    #         ))

    #     # Insert Other Data Sources into other_data_sources_table
    #     for source in session.get('other_data_sources', []):
    #         cursor.execute("""
    #             INSERT INTO other_data_sources_table (dataset_name, dataset_description, dataset_type, valid_from_date, valid_to_date)
    #             VALUES (%s, %s, %s, %s, %s)
    #         """, (
    #             source.get('name'),
    #             source.get('description'),
    #             source.get('type'),
    #             source.get('valid_from'),
    #             source.get('valid_to')
    #         ))

    #     # Insert Platforms into platforms_table
    #     for platform in session.get('platforms', []):
    #         cursor.execute("""
    #             INSERT INTO platforms_table (platform_name, platform_description, valid_from_date, valid_to_date)
    #             VALUES (%s, %s, %s, %s)
    #         """, (
    #             platform.get('name'),
    #             platform.get('description'),
    #             platform.get('valid_from'),
    #             platform.get('valid_to')
    #         ))

    #     # Commit the transaction
    #     conn.commit()

    # except Exception as e:
    #     print(f"Error inserting data into Snowflake: {e}")
    #     conn.rollback()  # Rollback in case of error
    #     return "There was an error with your submission. Please try again later."

    # finally:
    #     # Close the connection
    #     cursor.close()
    #     conn.close()

    # Clear session after submission
    session.clear()

    return redirect(url_for('thank_you'))  # Redirect to a thank you page



@app.route('/thank_you')
def thank_you():
    return "Thank you for submitting all data!"


if __name__ == '__main__':
    app.run(debug=True)
