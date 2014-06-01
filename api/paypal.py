import paypalrestsdk
import os

def read_full(e):
	f = open(e)
	n = f.readlines()[0].replace("\n","")
	f.close()
	return n

def do_paypal(l):
	amount = l[0]
	currency = l[1]

	paypalrestsdk.configure({
		"mode": "sandbox", # sandbox or live
		"client_id": os.environ.get('SECRET_KEY'),
		"client_secret": read_full("./client_secret")})

	payment = paypalrestsdk.Payment({
	  "intent":"sale",
	  "redirect_urls":{
		"return_url":"http://unhaltable.com/thanks",
		"cancel_url":"http://unhaltable.com/fuck_off"
	  },
	  "payer":{
		"payment_method":"paypal"
	  },
	  "transactions":[
		{
		  "amount":{
			"total":amount,
			"currency":currency
		  },
		  "description":"This is the payment transaction description."
		}
	  ]
	})
	
	if payment.create():
		redirect_url = "----"
		for link in payment.links:#Payer that funds a payment
			if link.method == "REDIRECT" :
				redirect_url=link.href
		return "Please go to ("+redirect_url+") to confirm your payment."
	else:
		return "Payment creation failed -- our bad :<"

def get_auth_token():
	return resp["access_token"]


if __name__ == "__main__":
	do_paypal(["12","USD"])
