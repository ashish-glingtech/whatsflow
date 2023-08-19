from marshmallow import Schema, fields ,validate, ValidationError
from models import Merchant, User, Service, Booking, Offer
from flask_marshmallow import Marshmallow 

ma = Marshmallow()

class MerchantSchema(Schema):
    name = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    mobile = fields.Int(required=True)
    country_code = fields.Int(required=True)
    class Meta:
        # Fields to expose
        model = Merchant
        fields = ("name", "first_name", "last_name", "mobile", "country_code")
        load_instance = True


class UserSchema(ma.Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    gender = fields.Str(required=True)
    mobile = fields.Int(required=True)
    otp = fields.Int(required=True)
    country_code = fields.Int(required=True)
    class Meta:
        # Fields to expose
        model = User
        fields = ("first_name", "last_name", "gender", "mobile",
                    "otp", "country_code")
        load_instance = True


class ServiceSchema(ma.Schema):
    merchant_id = fields.Int(required=True)
    name = fields.Str(required=True)
    cost = fields.Int(required=True)
    duration = fields.Str(required=True)
    is_fixed = fields.Str(required=True)
    class Meta:
        # Fields to expose
        model = Service
        fields = ("merchant_id", "name", "cost", "duration", "is_fixed")
        load_instance = True
        

class BookingSchema(ma.Schema):
    user_id = fields.Int(required=True)
    duration = fields.Str(required=True)
    status = fields.Str(required=True)
    class Meta:
        # Fields to expose
        model = Booking
        fields = ("user_id", "duration", "status")
        load_instance = True


class OfferSchema(ma.Schema):
    merchant_id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)
    class Meta:
        # Fields to expose
        model = Offer
        fields = ("merchant_id", "title", "description", "status")
        load_instance = True


merchant_schema = MerchantSchema()
user_schema = UserSchema()
service_schema = ServiceSchema()
booking_schema = BookingSchema()
offer_schema = OfferSchema()