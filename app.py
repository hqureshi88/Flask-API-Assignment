from flask import Flask, render_template, request, jsonify
from data import order
import math
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
  country_list = {'GB','FR', 'DE', 'NL', 'BE', 'Other'}
  # today = date.today()
  # today_date = today.strftime('%b-%d-%Y')
  new_id = len(order)+1
  print({new_id: request.form})
  if "name" in request.form:
    if request.form["insurance_required"].lower() == "true" and int(request.form["value"]) <= 10000:
        cost = int(request.form["value"])
        country_delivered = request.form["r_country_code"]
        if country_delivered == "GB":
          cost = round(cost*0.01, 2)
        elif country_delivered == "FR" or country_delivered == "DE" or country_delivered == "NL" or country_delivered == "BE":
          cost = round(cost*0.015, 2)
        else:
          cost = round(cost*0.04, 2)
        if cost < 9:
          cost = 9
    
        ipt_included_in_charge = cost - (cost/1.12)
        ipt_included_in_charge = round(ipt_included_in_charge, 2)
        dateTimeObj = datetime.now()
        order_url = "http://localhost:8080/order/" + str(new_id)
        order[new_id] = {
            "package": {
              "sender": {
                "name": request.form["name"],
                "street_address": request.form["street_address"],
                "city": request.form["city"],
                "country_code":'GB'
                },
              "recipient": {
                "name": request.form["r_name"],
                "street_address": request.form["r_street_address"],
                "city": request.form["r_city"],
                "country_code":request.form["r_country_code"]
                },
              "value": request.form["value"],
              "despatch_date": request.form["despatch_date"],
              "contents_declaration": request.form["contents_declaration"],
              "insurance_required": request.form["insurance_required"],
              "tracking_reference": request.form["tracking_reference"]
              },
              "order_url": order_url,
              "accepted_at": str(dateTimeObj),
              "insurance_provided": request.form["insurance_required"],
              "total_insurance_charge": cost,
              "ipt_included_in_charge": ipt_included_in_charge
            }
        return render_template("index.html", template_order=order, country_list = country_list)

  return render_template("index.html", template_order=order, country_list = country_list)

@app.route("/orders/<int:id>")
def orders(id):
  return render_template("order.html", 
  sender_name=order[id]["package"]["sender"]["name"],  
  sender_street=order[id]["package"]["sender"]["street_address"], 
  sender_city=order[id]["package"]["sender"]["city"], 
  sender_country=order[id]["package"]["sender"]["country_code"],
  recipient_name=order[id]["package"]["recipient"]["name"], 
  recipient_street=order[id]["package"]["recipient"]["street_address"], 
  recipient_city=order[id]["package"]["recipient"]["city"], 
  recipient_country=order[id]["package"]["recipient"]["country_code"],
  value=order[id]["package"]["value"],
  despatch_date=order[id]["package"]["despatch_date"],
  contents_declaration=order[id]["package"]["contents_declaration"],
  insurance_required=order[id]["package"]["insurance_required"],
  tracking_reference=order[id]["package"]["tracking_reference"],
  accepted_at = order[id]['accepted_at'],
  insurance_provided = order[id]['insurance_provided'],
  total_insurance_charge = order[id]['total_insurance_charge'],
  ipt_included_in_charge = order[id]['ipt_included_in_charge'])

if __name__ == '__main__':
    app.run(debug=True)