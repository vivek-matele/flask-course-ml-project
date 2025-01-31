from flask import Flask,url_for,render_template
import pandas as pd
import joblib 
from forms import InputForm
app=Flask(__name__)
app.config['SECRET_KEY']='secret_key'
model=joblib.load('model.joblib')
 
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',title='Home')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    form = InputForm()
    message = ""  # Default empty message

    if form.validate_on_submit():
        print("Form submitted successfully")  # Debugging

        try:
            # Create DataFrame with corrected types
            X_new = pd.DataFrame(dict(
                airline=[str(form.airline.data)],
                date_of_journey=[form.date_of_journey.data.strftime("%Y-%m-%d")],
                source=[str(form.source.data)],
                destination=[str(form.destination.data)],
                dep_time=[form.dep_time.data.strftime("%H:%M:%S")],
                arrival_time=[form.arrival_time.data.strftime("%H:%M:%S")],
                duration=[float(form.duration.data)],
                total_stops=[int(form.total_stops.data)],
                additional_info=[str(form.additional_info.data)],
            ))

            print(X_new)  # Debugging
            print(X_new.dtypes)  # Debugging

            # Make Prediction
            prediction = model.predict(X_new)[0]
            message = f"The predicted price is {prediction:,.0f} INR"

        except Exception as e:
            print("Prediction error:", str(e))  # Debugging
            message = "An error occurred during prediction."

    else:
        print("Form validation failed")  # Debugging
        print(form.errors)  # Show errors
        message = "Please provide valid input details"

    return render_template('predict.html', title='Predict', form=form, output=message)


if __name__=='__main__':
    app.run(debug=True)


