from flask import Flask, render_template, request, redirect, url_for
from pydantic.error_wrappers import ErrorWrapper
# from werkzeug.utils import redirect
from data import order
from datetime import datetime
from pydantic import BaseModel, ValidationError, validator
import re

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
  country_list = {'GB','FR', 'DE', 'NL', 'BE', 'Other'}

  def name_must_contain_space(name: str) -> str:
      if ' ' not in name:
          raise ValueError('Please enter your full senders and recipients name')
      return name.title()
  
  def address_must_contain_space(address: str) -> str:
      if ' ' not in address:
          raise ValueError('Please enter a valid address for both sender and recipient')
      return address

  def must_contain_city(city: str) -> str:
        if len(city) == 0:
            raise ValueError('Please enter name of city for both sender and recipient')
        return city.title()
  
  def insurance_limit(value: int) -> int:
        if value > 10000:
            raise ValueError('value is greater than £10000, unable to be insured')
        return value
  
  def correct_despatch_date(despatch_date: str) -> str:
        x = re.search("^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$", despatch_date)
        if not x:
            raise ValueError('Please enter appropriate date format')
        return despatch_date

  class SenderModel(BaseModel):
    s_name: str
    s_street_address: str
    s_city: str

    # validators
    _contain_spaces_name = validator('s_name', allow_reuse=True)(name_must_contain_space)
    _contain_spaces_address = validator('s_street_address', allow_reuse=True)(address_must_contain_space)
    _contain_city = validator('s_city', allow_reuse=True)(must_contain_city)

  class RecipientModel(BaseModel):
    r_name: str
    r_street_address: str
    r_city: str

    # validators
    _contain_spaces_name = validator('r_name', allow_reuse=True)(name_must_contain_space)
    _contain_spaces_address = validator('r_street_address', allow_reuse=True)(address_must_contain_space)
    _contain_city = validator('r_city', allow_reuse=True)(must_contain_city)
  
  class PackageModel(BaseModel):
    value: int
    despatch_date: str

    _insurance_limit = validator('value', allow_reuse=True)(insurance_limit)
    _despatch_date = validator('despatch_date', allow_reuse=True)(correct_despatch_date)
    

  if "name" in request.form:
    try:
      SenderModel(
        s_name = request.form["name"],
        s_street_address = request.form["street_address"],
        s_city = request.form["city"]
      )
      # print("accepted")
      RecipientModel(
        r_name = request.form["r_name"],
        r_street_address = request.form["r_street_address"],
        r_city = request.form["r_city"]
      )
      # print("accepted")
      PackageModel(
        value = int(request.form["value"]),
        despatch_date = request.form["despatch_date"]
      )
      # print("accepted")
    except ValidationError as e:
      error_output = []
      for error in e.args[0]:
        error_output.append(str(error.exc))
      print(error_output)
      # return redirect(url_for('index'))
      return render_template("index.html", error_output = error_output, template_order=order, country_list = country_list)

    # declare variables for insurance value and country code
    cost = int(request.form["value"])
    country_delivered = request.form["r_country_code"]
    

    # check if insurance is to be included by customer
    if int(request.form["insurance_required"]) == 1:
      if country_delivered == "GB":
        cost = round(cost*0.01, 2)
      elif country_delivered == "FR" or country_delivered == "DE" or country_delivered == "NL" or country_delivered == "BE":
        cost = round(cost*0.015, 2)
      else:
        cost = round(cost*0.04, 2)
      if cost < 9:
        cost = 9
    
    new_id = len(order)+1
    print({new_id: request.form})
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