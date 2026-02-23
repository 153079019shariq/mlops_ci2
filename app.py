from flask import Flask
import pickle
from flask import request

print("Display_the_name ", __name__)

## __name__ evaluate the name of the current module.
app = Flask(__name__)


@app.route("/ping/<username>", methods=["GET"])
def ping(username):
    return f"Hi ,{username}  is  working!!"


model_pickle = open("./mlops_demo/artefacts/classifier.pkl", "rb")
clf = pickle.load(model_pickle)
print("Loaded_the_model")


@app.route("/predict", methods=["POST"])
def prediction():
    """Returns loan application status using ML model"""
    loan_req = request.get_json()
    print(loan_req)
    if loan_req["Gender"] == "Male":
        Gender = 0
    else:
        Gender = 1
    if loan_req["Married"] == "Unmarried":
        Married = 0
    else:
        Married = 1
    if loan_req["Credit_History"] == "Unclear Debts":
        Credit_History = 0
    else:
        Credit_History = 1

    ApplicantIncome = loan_req["ApplicantIncome"]
    LoanAmount = loan_req["LoanAmount"]

    result = clf.predict(
        [[Gender, Married, ApplicantIncome, LoanAmount, Credit_History]]
    )

    if result == 0:
        pred = "Rejected"
    else:
        pred = "Approved"

    return {"loan_approval_status": pred}


if __name__ == "__main__":
    app.run(debug=True, port=8000)
