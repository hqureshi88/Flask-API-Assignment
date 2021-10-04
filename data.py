# recipes = {1: "fried egg", 2: "buttered toast"}
# types = {1: "Breakfast", 2: "Breakfast"}
# descriptions = {1: "Egg fried in butter", 2: "Toasted bread spread with butter"}
# ingredients = {1: ["1 pad of butter", "1 Egg", "A pinch of salt"], 2: ["1 pad of salted butter", "1 slice of bread"]}
# instructions = {1: {"Step 2": "Crack the egg into the buttered pan", "Step 5": "Serve egg after about a minute and a half", "Step 1": "Melt butter in pan over medium-low heat", "Step 4": "Flip egg after about a minute and a half", "Step 3": "Sprinke the pinch of salt onto cooking egg",},
#                 2: {"Step 3": "Put the pad of butter on the toasted bread", "Step 4": "After a minute spread the melted butter onto the bread", "Step 1": "Put the bread in the toaster", "Step 2": "Take the toast out of the toaster"}}
# comments = {1: ["Yummy!!", "Egg-cellent ;->"], 2: ["Toasty", "What a great recipe!"]}

# def add_ingredients(recipe_id=None, text=None):
#   if recipe_id and text:
#     text_list = text.split("\n")
#     ingredients[recipe_id] = text_list

# def add_instructions(recipe_id=None, text=None):
#   if recipe_id and text:
#     text_list = text.split("\n")
#     instructions_dict = {}
#     for i, instruction in enumerate(text_list):
#       instructions_dict["Step {}".format(i+1)] = instruction

#     instructions[recipe_id] = instructions_dict

order = {
1:{
  "package": {
    "sender": {
      "name": "Carole's Computers",
      "street_address": "123 Castle Street",
      "city": "Birmingham",
      "country_code": "GB"
    },
    "recipient": {
      "name": "Angela Schmidt",
      "street_address": "123 Schloßstraße",
      "city": "Berlin",
      "country_code": "DE"
    },
    "value": "1234.50",
    "despatch_date": "2021-09-01",
    "contents_declaration": "Laptop",
    "insurance_required": "true",
    "tracking_reference": "GBDE1244439090"
  },
  "order_url": "http://localhost:8080/order/1",
  "accepted_at": "2021-09-01T12:22:43.406768",
  "insurance_provided": "true",
  "total_insurance_charge": "18.52",
  "ipt_included_in_charge": "1.98"
},
2:{
  "package": {
    "sender": {
      "name": "Jim's Computers",
      "street_address": "345 Drive Street",
      "city": "Birmingham",
      "country_code": "GB"
    },
    "recipient": {
      "name": "Helga Milligan",
      "street_address": "345 Schloßstraße",
      "city": "Berlin",
      "country_code": "DE"
    },
    "value": "456.50",
    "despatch_date": "2021-09-02",
    "contents_declaration": "Laptop",
    "insurance_required": "true",
    "tracking_reference": "GBDE1231239090"
  },
  "order_url": "http://localhost:8080/order/1",
  "accepted_at": "2021-09-01T12:22:43.406768",
  "insurance_provided": "true",
  "total_insurance_charge": "18.52",
  "ipt_included_in_charge": "1.98"
}
}