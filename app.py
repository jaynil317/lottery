from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import session
# from passenger_wsgi import application
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token,jwt_required, get_jwt_identity
from datetime import datetime, timezone


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'mindstorm'  # Use a strong secret key!
jwt = JWTManager(app)  # You can make it any random string

CORS(app, supports_credentials=True)  # Allow requests from React frontend

# Dummy users database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u95nouvwthf5z:PatelJKR0410@abc13525.sg-host.com/dbydq3hshjghrw'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://my_user:my_password@yourserver.siteground.net/my_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
users = {}
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'pool_pre_ping': True
}
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
db = SQLAlchemy(app)

import random
from datetime import datetime

def generate_withdrawal_id(username):
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")  # e.g., 20250429134520
    random_number = random.randint(100, 999)                # e.g., 237
    return f"withdraw_{username}_{timestamp}_{random_number}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    # photo_url = db.Column(db.String(255))


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

class Utrnumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    utr=db.Column(db.String(12),nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

class Balance(db.Model):
    username = db.Column(db.String(80),primary_key=True, nullable=False)
    balance=db.Column(db.Float, default=10.0)

class Withdrawal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custom_id = db.Column(db.String(50), unique=True) 
    status = db.Column(db.String(50)) 
    upiId = db.Column(db.String(50))
    user_id = db.Column(db.Integer,nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # user = db.relationship('User', backref=db.backref('withdrawals', lazy=True))
# Example SQLAlchemy model
class SliderImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(500))  # Full URL or relative path
    # video_url = db.column(db.String(500))

class SliderVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String(500))  # Full URL or relative path

class LotteryDetail1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    prize = db.Column(db.String(20), nullable=False)
    prizeUnit = db.Column(db.String(20), nullable=False)
    drawDate = db.Column(db.String(20), nullable=False)
    drawTime = db.Column(db.String(20), nullable=False)
    ticketPrice = db.Column(db.String(20), nullable=False)
    winningAmount = db.Column(db.String(20), nullable=True)  # Note: corrected spelling
    contestFilled = db.Column(db.Integer, nullable=False)
    contestSize = db.Column(db.Integer, nullable=False)
    firstPrize = db.Column(db.String(20), nullable=False)
    secondPrize = db.Column(db.String(20), nullable=False)
    thirdPrize = db.Column(db.String(20), nullable=False)
    percent30return=db.Column(db.Integer,nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'prize': self.prize,
            'prizeUnit': self.prizeUnit,
            'drawDate': self.drawDate,
            'drawTime': self.drawTime,
            'ticketPrice': self.ticketPrice,
            'winningAmount': self.winningAmount,
            'contestFilled': self.contestFilled,
            'contestSize': self.contestSize,
            'firstPrize': self.firstPrize,
            'secondPrize': self.secondPrize,
            'thirdPrize': self.thirdPrize,
            'percent30return': self.percent30return
        }
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), nullable=False)
    lottery_id = db.Column(db.Integer, nullable=False)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "User already exists"}), 400

    new_user = User(email=email, password=password)
    balance1=Balance(username=email,balance=10.0)
    db.session.add(new_user)
    db.session.add(balance1)
    db.session.commit()

    return jsonify({"success": True, "message": "User registered successfully"}), 200 

from flask import jsonify

@app.route('/slider-images', methods=['GET'])
def get_slider_images():
    images = SliderImage.query.all()
    image_urls = [img.image_url for img in images]
    return jsonify(image_urls)

@app.route('/slider-video', methods=['GET'])
def get_slider_video():
    images = SliderVideo.query.all()
    video_url = [img.video_url for img in images]
    # video_url=images.video_url
    return jsonify(video_url)

@app.route('/status', methods=['GET'])
def status():
    is_logged_in = session.get('logged_in', False)
    return jsonify({'loggedIn': is_logged_in}), 200

@app.route('/lottery-details', methods=['GET'])
def get_lottery_details():
    details = LotteryDetail1.query.all()
    return jsonify([detail.to_dict() for detail in details])

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email, password=password).first()
    
    balance=Balance.query.filter_by(username=email).first()
    if user:
        access_token = create_access_token(identity=user.email)
        return jsonify({'access_token': access_token,'wallet_balance': balance.balance}), 200

    return jsonify({'message': 'Invalid credentials'}), 401     

@app.route('/profile', methods=['GET', 'POST'])
@jwt_required()
def profile():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    profile1 = Profile.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if request.method == 'GET':
        if profile1:
            return jsonify({
                'first_name': profile1.first_name,
                'last_name': profile1.last_name,
                'email': profile1.email,
                'phone': profile1.phone
            })
        else:
        # Return empty fields if no profile exists yet
            return jsonify({
                'first_name': '',
                'last_name': '',
                'email': email,
                'phone': ''
            })
    if profile1:
    # Update existing profile
        profile1.first_name = first_name
        profile1.last_name = last_name
        profile1.phone = phone
    else:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get('phone')
        profile = Profile(email=email,first_name=first_name,last_name=last_name,phone=phone)
        db.session.add(profile)
    db.session.commit()

    return jsonify({'message': 'Profile updated successfully'})

@app.route('/addfunds1', methods=['POST'])
@jwt_required()
def addfunds1():
        username = get_jwt_identity()
        balance=Balance.query.filter_by(username=username).first()
        # print("jk 1")
        if not username:
            return jsonify({'message': 'User not logged in'}), 401

        if balance is not None :
            return jsonify({'balance': balance.balance}), 200
        
        # return jsonify({'message': 'Amount is required'}), 400



@app.route('/addfunds', methods=['POST'])
@jwt_required()
def addfunds():
    # try:
        username = get_jwt_identity()
        balance=Balance.query.filter_by(username=username).first()
        print("jk 1")
        # if balance is not None :
        #     return jsonify({'balance': balance.balance}), 200
        if not username:
            return jsonify({'message': 'User not logged in'}), 401
        print("kk 1")
        data = request.get_json()
        amount = data.get('amount')
        
        # availablebalance=data.get('availablebalance')

        if not amount:
            return jsonify({'message': 'Amount is required'}), 400

        # username = session['user']
        donation = Donation(username=username, amount=amount)
        print("hello2")
        db.session.add(donation)
        # balance=Balance.query.filter_by(username=username).first()
        # jsonify({'balance': balance.balance}), 200
        
        # db.session.add(donation)
        db.session.commit()

        return jsonify({'message': 'payment was recorded'}), 200
    # except Exception as e:
    #     return jsonify({'message': 'adding failed', 'error': str(e)}), 500


@app.route('/support-tickets', methods=['POST'])
@jwt_required()
def create_support_ticket():
    try:
        user_id = get_jwt_identity()
        print("User ID from JWT:", user_id) 
        data = request.get_json()

        subject = data.get('subject')
        message = data.get('message')
        timestamp = data.get('timestamp')  # optional, you can rely on server time

        if not subject or not message:
            return jsonify({'error': 'Subject and message are required'}), 400

        ticket = SupportTicket(
            user_id=user_id,
            subject=subject,
            message=message,
            timestamp=timestamp or datetime.utcnow()
        )

        db.session.add(ticket)
        db.session.commit()

        return jsonify({
        
            'message': ticket.message
            
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'support request failed', 'error': str(e)}), 500


@app.route('/support-tickets1', methods=['GET'])
@jwt_required()
def get_support_tickets1():
    try:
        user_id = get_jwt_identity()
        print("User ID (GET):", user_id)  # Optional debug

        tickets = SupportTicket.query.filter_by(user_id=user_id).order_by(SupportTicket.timestamp.desc()).all()

        return jsonify([
            {
                'id': ticket.id,
                'subject': ticket.subject,
                'message': ticket.message,
                'timestamp': ticket.timestamp.isoformat()
            }
            for ticket in tickets
        ])

    except Exception as e:
        return jsonify({'message': 'failed', 'error': str(e)}), 500

@app.route('/utr', methods=['POST'])
@jwt_required()
def utr():
    username = get_jwt_identity()
    if not username:
        return jsonify({'message': 'User not logged in'}), 401

    data = request.get_json()
    utr=data.get('utrNumber')
    if not utr:
        return jsonify({'message': 'UTR NUMBER is required'}), 400
    utrnumber= Utrnumber(username=username, utr=utr)
    db.session.add(utrnumber)
    db.session.commit() 
    return jsonify({'message': 'submitted'}), 200  


@app.route('/withdraw', methods=['POST'])
@jwt_required()
def withdraw():
    try:
        # print("Start withdrawal-5")
        user_id = get_jwt_identity()
        # print("Start withdrawal-4")
        data = request.get_json()
        # print("Start withdrawal-3")
        amount = data.get('amount')
        upiId=data.get('upiId')

        # print("Start withdrawal-2")

        if amount is None or amount <= 0 or upiId is None:
            return jsonify({'message': 'Invalid withdrawal amount'}), 400
        
        # print("Start withdrawal-1")

        user = User.query.filter_by(email=user_id).first()
        balance2 = Balance.query.filter_by(username=user_id).first()

        # print("Start withdrawal0")

        if not user:
            return jsonify({'message': 'User not found'}), 404

        if balance2.balance < amount:
            return jsonify({'message': 'Insufficient balance'}), 400

        # print("Start withdrawal1")

        balance2.balance -= amount


        withdrawal_id = generate_withdrawal_id(user_id)

        # print("Start withdrawal2")

        # Save withdrawal history
        withdrawal_entry = Withdrawal(
            custom_id=withdrawal_id, 
            status="pending", 
            upiId=upiId, 
            user_id=user_id, 
            amount=amount
            )
        # print("Start withdrawal3")

        db.session.add(withdrawal_entry)

        # print("Start withdrawal4")

        db.session.commit()

        return jsonify({'message': 'Withdrawal successful', 'new_balance': balance2.balance})
    except Exception as e:
        return jsonify({'message': 'Withdrawal failed', 'error': str(e)}), 500


@app.route('/withdrawals', methods=['GET'])
@jwt_required()
def get_withdrawals():
    user_id = get_jwt_identity()
    withdrawals = Withdrawal.query.filter_by(user_id=user_id).order_by(Withdrawal.timestamp.desc()).all()

    history = [
        {'amount': w.amount, 'timestamp': w.timestamp.isoformat(),'custom':w.custom_id,'status':w.status,'upiId':w.upiId}
        for w in withdrawals
    ]
    return jsonify(history)


@app.route('/buy-ticket', methods=['POST'])
@jwt_required()
def buy_ticket():
    user_email = get_jwt_identity()
    data = request.get_json()
    lottery_id = data.get('lottery_id')

    if not lottery_id:
        return jsonify({'message': 'Lottery ID required'}), 400

    user_balance = Balance.query.filter_by(username=user_email).first()
    lottery = LotteryDetail1.query.filter_by(id=lottery_id).first()

    if not user_balance or not lottery:
        return jsonify({'message': 'Invalid user or lottery'}), 400

    ticket_price = float(lottery.ticketPrice.replace('₹', '').strip())


    if user_balance.balance < ticket_price:
        return jsonify({'message': 'Insufficient balance'}), 400

    # Deduct balance
    user_balance.balance -= ticket_price
    lottery.contestFilled += 1
    db.session.add(lottery)
    # db.session.add(Balance)

    # Generate unique ticket number
    ticket_number = f"TKT{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}"
     # NEW: Prevent buying if contest is full
    if lottery.contestFilled >= lottery.contestSize:
        return jsonify({'message': 'This lottery contest is already full'}), 400

    # Create and save ticket
    ticket = Ticket(user_email=user_email, lottery_id=lottery_id, ticket_number=ticket_number)
    db.session.add(ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket purchased', 'ticket_number': ticket_number, 'new_balance': user_balance.balance})


@app.route('/my-tickets', methods=['GET'])
@jwt_required()
def my_tickets():
    user_email = get_jwt_identity()
    tickets = Ticket.query.filter_by(user_email=user_email).order_by(Ticket.timestamp.desc()).all()

    ticket_data = []
    for t in tickets:
        lottery = LotteryDetail1.query.filter_by(id=t.lottery_id).first()
        ticket_data.append({
            'ticket_number': t.ticket_number,
            'lottery_id': t.lottery_id,
            'lottery_title': lottery.title if lottery else '',
            'ticket_price': lottery.ticketPrice if lottery else '',
            'timestamp': t.timestamp.isoformat()
        })

    return jsonify(ticket_data)



@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'message': 'Logged out successfully'}), 200
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
