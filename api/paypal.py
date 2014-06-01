import paypalrestsdk

def read_full(e):
	f = open(e)
	n = f.readlines()[0].replace("\n","")
	f.close()
	return n

def do_paypal(l):
	amount = l[0]
	currency = l[1]

	resp = paypalrestsdk.configure({
	  	"mode": "sandbox", # sandbox or live
	  	"client_id": "ASADDBDt4pU4eFXwJq16hXlXl5keoZ7VbJyasjinFsdFnILS_4MkMhDcUqtB",
	  	"client_secret": read_full("./client_secret")})


	payment = paypalrestsdk.Payment({
	  "intent": "sale",
	  "payer": {
    "payment_method": "paypal" },
	  "transactions": [{
	    "item_list": {
	      "items": [{
	        "name": "txti donation",
	        "sku": "item",
	        "price": amount,
	        "currency": currency,
	        "quantity": 1 }]},
	    "amount": {
	      "total": "1.00",
	      "currency": "USD" },
	    "description": "donation to the unhaltable//txti team." }]})

	
	jsonresp = payment.create()

	return "go to ("+jsonresp['approval url']+") to confirm payment"


def get_auth_token():

	return resp["access_token"]

if __name__ == "__main__":
	do_paypal(["12","USD"])
