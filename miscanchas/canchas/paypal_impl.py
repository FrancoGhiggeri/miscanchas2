from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment 
from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCaptureRequest
from decouple import config

class PayPalClient:
    def __init__(self):
        self.client_id = config('PAYPAL_CLIENT_ID')
        self.client_secret = config('PAYPAL_SECRET_KEY')
        if bool(config('TESTING_PAYMENT')):
            self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        else:
            self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)


class GetOrder(PayPalClient):
    def get_order(self, order_id):
        request = OrdersGetRequest(order_id)
        response = self.client.execute(request)
        return response


class CaptureOrder(PayPalClient):
    def capture_order(self, order_id, debug=False):
        request = OrdersCaptureRequest(order_id)
        response = self.client.execute(request)
        if debug:
            print ('Status Code: ', response.status_code)
            print ('Status: ', response.result.purchase_units[0].payments.captures[0].status)
            print ('Order ID: ', response.result.id)
            print ('Links: ')
        return response