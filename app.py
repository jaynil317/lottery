from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import session
# from passenger_wsgi import application
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token,jwt_required, get_jwt_identity
from datetime import datetime, timezone
from datetime import date


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
    random_number = random.randint(100, 99999999)                # e.g., 237
    return f"withdraw_{username}_{timestamp}_{random_number}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo=db.Column(db.String(500))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo=db.Column(db.String(500))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role=db.Column(db.String(255))
    status=db.column(db.String(255))

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
    status = db.Column(db.String(50))
    amount = db.Column(db.Float, nullable=False)

class Balance(db.Model):
    username = db.Column(db.String(80),primary_key=True, nullable=False)
    balance=db.Column(db.Float, default=10.0)

class Withdrawal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custom_id = db.Column(db.String(50), unique=True) 
    status = db.Column(db.String(50)) 
    upiId = db.Column(db.String(50))
    user_id = db.Column(db.String(50),nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # user = db.relationship('User', backref=db.backref('withdrawals', lazy=True))
# Example SQLAlchemy model
class SliderImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    status = db.Column(db.String(25))  # Full URL or relative path
    # video_url = db.column(db.String(500))

class SmallSliderImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    status = db.Column(db.String(25))

class SliderVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    description = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    status = db.Column(db.String(25))  # Full URL or relative path

class LotteryDetail1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    prize = db.Column(db.Integer, nullable=False)
    prizeUnit = db.Column(db.String(20), nullable=False)
    drawDate = db.Column(db.String(20), nullable=False)
    drawTime = db.Column(db.String(20), nullable=False)
    ticketPrice = db.Column(db.String(20), nullable=False)
    winningAmount = db.Column(db.String(20), nullable=True)  # Note: corrected spelling
    contestFilled = db.Column(db.Integer)
    contestSize = db.Column(db.Integer, nullable=False)
    firstPrize = db.Column(db.Integer, nullable=False)
    secondPrize = db.Column(db.Integer, nullable=False)
    thirdPrize = db.Column(db.Integer, nullable=False)
    percent30return=db.Column(db.Integer,nullable=False)
    usersToReturn=db.Column(db.Integer,default=0,nullable=False)

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
            'percent30return': self.percent30return,
            'usersToReturn': self.usersToReturn
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

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

# class Winner(db.Model):
#     __tablename__ = 'winners'

#     id = db.Column(db.Integer, primary_key=True)
#     photo = db.Column(db.String(255), nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     amount = db.Column(db.Float, nullable=False)
#     date = db.Column(db.Date, nullable=False)

#     def __repr__(self):
#         return f"<Winner {self.name} - {self.amount}>"

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "photo": self.photo,
#             "name": self.name,
#             "amount": str(self.amount),
#             "date": self.date.strftime("%Y-%m-%d")
#         }

class Winner(db.Model):
    __tablename__ = 'winners'

    id = db.Column(db.Integer, primary_key=True)
    
    contestTitle = db.Column(db.String(255), nullable=False)

    
    name = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(500))  # optional field

    position = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)  # assuming prize can have decimals

    date = db.Column(db.String(100), nullable=False)  # or use db.Date if using actual dates
    status = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            
            "contestTitle": self.contestTitle,
            
            "name": self.name,
            "photo": self.photo,
            "position": self.position,
            "amount": self.amount,
            "date": self.date,
            "status": self.status
        }

class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    image_url = db.Column(db.Text, nullable=False)  # base64-encoded image
    status = db.Column(db.String(20), default='Active')


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
    images = SliderImage.query.filter_by(status='Active').all()
    image_urls = [img.image_url for img in images]
    return jsonify(image_urls)

@app.route('/small-slider-images', methods=['GET'])
def get_small_slider_images():
    images = SmallSliderImage.query.filter_by(status='Active').all()
    image_urls = [img.image_url for img in images]
    return jsonify(image_urls)

@app.route('/slider-video', methods=['GET'])
def get_slider_video():
    images = SliderVideo.query.filter_by(status='Active').all()
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

@app.route('/adminlogin', methods=['POST'])
def admin_login():
     # Assuming you have a User model for regular users
    all_users = AdminUser.query.all()
    users_list = [{
            'id': u.id,
            'name': u.name,
            'email': u.email,
            'role': u.role,
            'status': u.status
    } for u in all_users]

    return jsonify({         
            'users': users_list
    }), 200

    

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
    amount=data.get('amount')
    if not utr:
        return jsonify({'message': 'UTR NUMBER is required'}), 400
    utrnumber= Utrnumber(username=username, utr=utr,status='pending',amount=amount)
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
    try:
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
        
        # NEW: Prevent buying if contest is full
        if lottery.contestFilled >= lottery.contestSize:
            return jsonify({'message': 'This lottery contest is already full'}), 400
        
        lottery.contestFilled += 1
        db.session.add(lottery)
        
        # db.session.add(Balance)

        # Generate unique ticket number
        ticket_number = f"TKT{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}"
        

        # Create and save ticket
        
        ticket = Ticket(user_email=user_email, lottery_id=lottery_id, ticket_number=ticket_number)
        
        db.session.add(ticket)
        db.session.commit()

        return jsonify({'ticket_number': ticket_number, 'new_balance': user_balance.balance, "success": True})
    except Exception as j:
        return jsonify({'error': 'Invalid request', 'details': str(j)}), 400



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



@app.route('/result', methods=['POST'])
# @jwt_required()
def get_result_by_post():
    # user_email = get_jwt_identity()
    data = request.get_json()
    date_str = data.get('date')
    # print(date_str)

    try:
        query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        # print(query_date)
        result = Result.query.filter_by(date=query_date).first()
        if result:
            return jsonify({'image_url': result.image_url})
        else:
            return jsonify({'image_url': None}), 404
    except:
        return jsonify({'error': 'Invalid request'}), 400


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/admin_users', methods=['GET'])
def get_users():
    # users = User.query.all()
    # # convert each model to a plain dict
    # return jsonify([{
    #     'id': u.id,
    #     'email': u.email,
    #     'password' : u.password,
    #     'photo' : u.photo
    #     # don't include password
    # } for u in users]), 200
    users = User.query.all()
    profiles = {p.email: p.first_name for p in Profile.query.all()}
    balances = {b.username: b.balance for b in Balance.query.all()}

    user_list = []
    for u in users:
        name = profiles.get(u.email, "Unknown")
        balance = balances.get(u.email, 0.0)
        user_list.append({
            'id': u.id,
            'email': u.email,
            'password': u.password,
            'photo': u.photo,
            'name': name,
            'balance': balance
        })
    return jsonify(user_list), 200

@app.route('/admin_deposits', methods=['GET'])
def admin_deposits():
    # users = User.query.all()
    # # convert each model to a plain dict
    # return jsonify([{
    #     'id': u.id,
    #     'email': u.email,
    #     'password' : u.password,
    #     'photo' : u.photo
    #     # don't include password
    # } for u in users]), 200
    deposits = Utrnumber.query.all()
    return jsonify([{

        'id' : u.id,
        'userName': u.username,
        'userPhoto': "https://randomuser.me/api/portraits/women/12.jpg",
        'userId': u.id,
        'amount' : u.amount ,
        'currency': "INR",
        'method': "UPI",
        'time' : u.timestamp,
        'utrNumber' : u.utr,
        'status' : u.status
               # don't include password
    } for u in deposits]), 200

@app.route('/update_deposit_status', methods=['POST'])
def update_deposit_status():
    data = request.get_json()
    deposit_id = data.get('id')
    username = data.get('userName')
    amount = data.get('amount')
    new_status = data.get('status')

    deposit = Utrnumber.query.filter_by(id=deposit_id).first()
    if not deposit:
        return jsonify({'error': 'Deposit not found'}), 404

    if new_status == 'Delete':
        deposit = Utrnumber.query.filter_by(id=deposit_id).first()
        if not deposit:
            return jsonify({'error': 'Deposit not found'}), 404
        db.session.delete(deposit)
        db.session.commit()
        return jsonify({'message': f'Deposit ID {deposit_id} status updated to {new_status}'}), 200

    if new_status == 'Completed':
        balances = Balance.query.filter_by(username=username).first()
        balances.balance += amount
        db.session.add(balances)
        deposit.status = new_status
        db.session.commit()
        return jsonify({'message': f'Deposit ID {deposit_id} status updated to {new_status}'}), 200

    deposit.status = new_status

    db.session.commit()
    return jsonify({'message': f'Deposit ID {deposit_id} status updated to {new_status}'}), 200



    # return jsonify(user_list), 200
@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.get_json()
    id = data.get('userId')
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'users deleted'}), 200

@app.route('/add_deposit', methods=['POST'])
def add_deposit():
    data = request.get_json()

    new_deposit = Utrnumber(
        username=data.get('userName'),
        amount=data.get('amount'),
        utr=data.get('utrNumber'),
        status='pending',  # default status
        timestamp=datetime.utcnow()
    )
    db.session.add(new_deposit)
    db.session.commit()

    return jsonify({'message': 'Deposit added successfully'}), 201

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    
    new_user = User(
        photo=data.get('photo'),
        email=data.get('email'),
        password=data.get('password')
        # status='pending',  # default status
        # timestamp=datetime.utcnow()
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'user added successfully'}), 201

@app.route('/admin_withdrawals', methods=['GET'])
def admin_withdrawals():
    # users = User.query.all()
    # # convert each model to a plain dict
    # return jsonify([{
    #     'id': u.id,
    #     'email': u.email,
    #     'password' : u.password,
    #     'photo' : u.photo
    #     # don't include password
    # } for u in users]), 200
    deposits = Withdrawal.query.all()
    return jsonify([{

        'id' : u.id,
        'userName': u.user_id,
        'userPhoto': "https://randomuser.me/api/portraits/men/11.jpg",
        'userId': u.custom_id,
        'upiId' : u.upiId,
        'amount' : u.amount ,
        'currency': "INR",
        'method': "UPI",
        'date' : u.timestamp,
        
        'status' : u.status
               # don't include password
    } for u in deposits]), 200

@app.route('/add_withdrawal', methods=['POST'])
def add_withdrawal():
    data = request.get_json()
    id=generate_withdrawal_id(data.get('userName'))
    new_deposit = Withdrawal(
        user_id=data.get('userName'),
        custom_id=id,
        amount=data.get('amount'),
        upiId=data.get('upiId'),
        status='pending',  # default status
        timestamp=datetime.utcnow()
    )
    db.session.add(new_deposit)
    db.session.commit()

    return jsonify({'message': 'Deposit added successfully'}), 201


@app.route('/update_withdraw_status', methods=['POST'])
def update_withdraw_status():
    data = request.get_json()
    withdraw_id = data.get('custom_id')
    username = data.get('userName')
    # print(username)
    amount = data.get('amount')
    # print(amount)
    new_status = data.get('status')

    deposit = Withdrawal.query.filter_by(custom_id=withdraw_id).first()
    if not deposit:
        return jsonify({'error': 'withdraw not found'}), 404

    if new_status == 'Delete':
        # deposit = Utrnumber.query.filter_by(id=deposit_id).first()
        # if not deposit:
        #     return jsonify({'error': 'Deposit not found'}), 404
        if deposit.status == 'Rejected':
            deposit.status = new_status
            db.session.add(deposit)
            db.session.commit()
            return jsonify({'message': f'Deposit ID {withdraw_id} status updated to {new_status}'}), 200

        if deposit.status == 'Completed':
            deposit.status = new_status
            db.session.add(deposit)
            db.session.commit()
            return jsonify({'message': f'Deposit ID {withdraw_id} status updated to {new_status}'}), 200
        
        balances = Balance.query.filter_by(username=username).first()
        # print(balances)
        balances.balance += amount
        db.session.add(balances)
        deposit.status = new_status
        db.session.add(deposit)
        db.session.commit()
        return jsonify({'message': f'Deposit ID {withdraw_id} status updated to {new_status}'}), 200

    if new_status == 'Rejected':
        balances = Balance.query.filter_by(username=username).first()
        print(balances)
        balances.balance += amount
        db.session.add(balances)
        deposit.status = new_status
        db.session.commit()
        return jsonify({'message': f'Deposit ID {withdraw_id} status updated to {new_status}'}), 200

    deposit.status = new_status

    db.session.commit()
    return jsonify({'message': f'Deposit ID {withdraw_id} status updated to {new_status}'}), 200

@app.route('/admin_big_slider', methods=['GET'])
def admin_big_slider():
    slider = SliderImage.query.all()
    return jsonify([{

        'id' : u.id,
        'title': u.title,
        'description': u.description,
        'image': u.image_url,
        'status' : u.status
               # don't include password
    } for u in slider]), 200

@app.route('/edit_bigslider', methods=['POST'])
def edit_bigslider():
    data = request.get_json()
    id = data.get('id')
    title = data.get('title')
    description = data.get('description')
    image= data.get('image')
    status = data.get('status')
    # print(description)
    bigslider = SliderImage.query.filter_by(id=id).first()
    if not bigslider:
        return jsonify({'error': 'bigslider not found'}), 404
    bigslider.title=title
    bigslider.description=description
    bigslider.image_url=image
    bigslider.status=status
    db.session.add(bigslider)
    db.session.commit()
    return jsonify({'message': 'bidslider changed'}), 200

@app.route('/delete_bigslider', methods=['POST'])
def delete_bigslider():
    data = request.get_json()
    id = data.get('id')
    big_slider = SliderImage.query.filter_by(id=id).first()
    if not big_slider:
        return jsonify({'error': 'big_slider not found'}), 404
    db.session.delete(big_slider)
    db.session.commit()
    return jsonify({'message': 'big_slider deleted'}), 200 

@app.route('/add_bigslider', methods=['POST'])
def add_bigslider():
    try:
        data = request.get_json()
        id = data.get('id')
        title = data.get('title')
        description = data.get('description')
        image= data.get('image')
        status = data.get('status')
        big_slider = SliderImage(title=title,description=description,image_url=image,status=status)
        db.session.add(big_slider)
        db.session.commit()
        return jsonify({'message': 'big_slider added'}), 200
    except e as exception:
        return jsonify({'error': 'Invalid request'}), 400

@app.route('/admin_small_slider', methods=['GET'])
def admin_small_slider():
    slider = SmallSliderImage.query.all()
    return jsonify([{

        'id' : u.id,
        'title': u.title,
        'description': u.description,
        'image': u.image_url,
        'status' : u.status
               # don't include password
    } for u in slider]), 200

@app.route('/edit_smallslider', methods=['POST'])
def edit_smallslider():
    data = request.get_json()
    id = data.get('id')
    title = data.get('title')
    description = data.get('description')
    image= data.get('image')
    status = data.get('status')
    # print(description)
    smallslider = SmallSliderImage.query.filter_by(id=id).first()
    if not smallslider:
        return jsonify({'error': 'smallslider not found'}), 404
    smallslider.title=title
    smallslider.description=description
    smallslider.image_url=image
    smallslider.status=status
    db.session.add(smallslider)
    db.session.commit()
    return jsonify({'message': 'smallslider changed'}), 200

@app.route('/delete_smallslider', methods=['POST'])
def delete_smallslider():
    data = request.get_json()
    id = data.get('id')
    small_slider = SmallSliderImage.query.filter_by(id=id).first()
    if not small_slider:
        return jsonify({'error': 'small_slider not found'}), 404
    db.session.delete(small_slider)
    db.session.commit()
    return jsonify({'message': 'small_slider deleted'}), 200 

@app.route('/add_smallslider', methods=['POST'])
def add_smallslider():
    try:
        data = request.get_json()
        id = data.get('id')
        title = data.get('title')
        description = data.get('description')
        image= data.get('image')
        status = data.get('status')
        small_slider = SmallSliderImage(title=title,description=description,image_url=image,status=status)
        db.session.add(small_slider)
        db.session.commit()
        return jsonify({'message': 'small_slider added'}), 200
    except:
        return jsonify({'error': 'Invalid request'}), 400

@app.route('/admin_video', methods=['GET'])
def admin_video():
    slider = SliderVideo.query.all()
    return jsonify([{

        'id' : u.id,
        'title': u.title,
        'description': u.description,
        'videoUrl': u.video_url,
        'status' : u.status
               # don't include password
    } for u in slider]), 200

@app.route('/edit_video', methods=['POST'])
def edit_video():
    data = request.get_json()
    id = data.get('id')
    title = data.get('title')
    description = data.get('description')
    videoUrl= data.get('videoUrl')
    status = data.get('status')
    # print(description)
    video = SliderVideo.query.filter_by(id=id).first()
    if not video:
        return jsonify({'error': 'video not found'}), 404
    video.title=title
    video.description=description
    video.video_url=videoUrl
    video.status=status
    db.session.add(video)
    db.session.commit()
    return jsonify({'message': 'video changed'}), 200

@app.route('/delete_video', methods=['POST'])
def delete_video():
    data = request.get_json()
    id = data.get('id')
    video = SliderVideo.query.filter_by(id=id).first()
    if not video:
        return jsonify({'error': 'video not found'}), 404
    db.session.delete(video)
    db.session.commit()
    return jsonify({'message': 'video deleted'}), 200 

@app.route('/add_video', methods=['POST'])
def add_video():
    try:
        data = request.get_json()
        id = data.get('id')
        title = data.get('title')
        description = data.get('description')
        video= data.get('videoUrl')
        status = data.get('status')
        video = SliderVideo(title=title,description=description,video_url=video,status=status)
        db.session.add(video)
        db.session.commit()
        return jsonify({'message': 'video added'}), 200
    except:
        return jsonify({'error': 'Invalid request'}), 400

@app.route('/admin_contest', methods=['GET'])
def admin_contest():
    # users = User.query.all()
    # # convert each model to a plain dict
    # return jsonify([{
    #     'id': u.id,
    #     'email': u.email,
    #     'password' : u.password,
    #     'photo' : u.photo
    #     # don't include password
    # } for u in users]), 200
    lottery = LotteryDetail1.query.all()
    return jsonify([{

        'id' : u.id,
        'title' : u.title,
        'prize' : u.prize,
        'prizeUnit' : u.prizeUnit,
        'drawDate' : u.drawDate,
        'ticketPrice' : u.ticketPrice ,
        'winningAmount' : u.winningAmount,
        'contestFilled' : u.contestFilled,
        'contestSize' : u.contestSize,
        'firstPrize' : u.firstPrize,
        'secondPrize' : u.secondPrize,
        'thirdPrize' : u.thirdPrize,
        'percent30return' : u.percent30return,
        'returnAmount' : u.percent30return,
        'usersToReturn' : u.usersToReturn
               # don't include password
    } for u in lottery]), 200

@app.route('/edit_contests', methods=['POST','PUT'])
def edit_contests():
    try:
        data = request.get_json()
        id = data.get('id')
        title = data.get('title')
        prize = data.get('prize')
        winningAmount= data.get('winningAmount')
        prizeUnit = data.get('prizeUnit')
        drawDate = data.get('drawDate')
        drawTime = data.get('drawTime')
        ticketPrice = data.get('ticketPrice')
        contestSize = data.get('contestSize')
        firstPrize = data.get('firstPrize')
        secondPrize = data.get('secondPrize')
        thirdPrize = data.get('thirdPrize')
        returnAmount = data.get('returnAmount')
        usersToReturn = data.get('usersToReturn')

        # print(description)
        contest = LotteryDetail1.query.filter_by(id=id).first()
        if not contest:
            return jsonify({'message': 'contest not found'}), 404
        contest.title=title
        contest.prize=f"₹ {prize}"
        # contest.video_url=videoUrl
        contest.winningAmount=f"₹ {winningAmount}"
        contest.prizeUnit=prizeUnit
        contest.drawDate=drawDate
        contest.drawTime=drawTime
        contest.ticketPrice=f"₹ {ticketPrice}"
        contest.contestSize=contestSize
        contest.firstPrize=firstPrize
        contest.secondPrize=secondPrize
        contest.thirdPrize=thirdPrize
        contest.returnAmount=returnAmount
        contest.usersToReturn=usersToReturn
        db.session.add(contest)
        db.session.commit()
        return jsonify({'message': 'contest changed'}), 200
    except e:
        return jsonify({'message': e}), 404

@app.route('/delete_contest', methods=['POST'])
def delete_contest():
    data = request.get_json()
    id = data.get('contestId')
    contests = LotteryDetail1.query.filter_by(id=id).first()
    if not contests:
        return jsonify({'error': 'contests not found'}), 404
    db.session.delete(contests)
    db.session.commit()
    return jsonify({'message': 'contests deleted'}), 200 

@app.route('/Add_contests', methods=['POST'])
def Add_contests():
    try:
        data = request.get_json()
        add_contest=LotteryDetail1(
                title = data.get('title'),prize = data.get('prize'),winningAmount= data.get('winningAmount'),prizeUnit = data.get('prizeUnit'),drawDate = data.get('drawDate'),drawTime = data.get('drawTime'),ticketPrice = data.get('ticketPrice'),contestSize = data.get('contestSize'),firstPrize = data.get('firstPrize'),secondPrize = data.get('secondPrize'),thirdPrize = data.get('thirdPrize'),percent30return = data.get('returnAmount'),usersToReturn = data.get('usersToReturn'),contestFilled = 0
        )
        db.session.add(add_contest)
        db.session.commit()
    
        return jsonify({'message': 'contest changed'}), 200
    except Exception as e:
        print("Error adding contest:", e)
        return jsonify({'message': 'something wrong'}), 500

@app.route('/winners', methods=['GET'])
def get_winners():
    winners = Winner.query.order_by(Winner.id).all()
    return jsonify([w.to_dict() for w in winners])

# @app.route('/add_winners', methods=['POST'])
# def add_winner():
#     data = request.get_json()
#     try:
#         new_winner = Winner(
#             photo=data.get('photo'),
#             name=data.get('name'),
#             amount=float(data.get('amount')),
#             date=datetime.strptime(data.get('date'), "%Y-%m-%d").date(),
#             status=data.get('status'),
#             contestTitle=data.get('contestTitle'),
#             position=data.get('position')
#         )
#         db.session.add(new_winner)
#         db.session.commit()
#         return jsonify({"message": "Winner added successfully!"}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
@app.route('/add_winners', methods=['POST'])
def add_winners():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # If it's a single object, convert it into a list
        winners_data = data if isinstance(data, list) else [data]
        new_winners = []

        for entry in winners_data:
            new_winner = Winner(
                photo=entry.get('photo'),
                name=entry.get('name'),
                amount=float(entry.get('amount')),
                date=datetime.strptime(entry.get('date'), "%Y-%m-%d").date(),
                status=entry.get('status'),
                contestTitle=entry.get('contestTitle'),
                position=entry.get('position')
            )
            db.session.add(new_winner)
            new_winners.append(new_winner)

        db.session.commit()
        return jsonify({"message": f"{len(new_winners)} winner(s) added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# @app.route('/winners/<int:winner_id>', methods=['DELETE'])
# def delete_winner(winner_id):
#     try:
#         winner = Winner.query.get(winner_id)
#         if not winner:
#             return jsonify({"error": "Winner not found"}), 404

#         db.session.delete(winner)
#         db.session.commit()
#         return jsonify({"message": "Winner deleted successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@app.route('/delete_winners/<int:winner_id>', methods=['POST'])
def delete_winner(winner_id):
    try:
        winner = db.session.get(Winner, winner_id)  # ✅ modern SQLAlchemy 2.0+ way
        if not winner:
            return jsonify({"error": "Winner not found"}), 404

        db.session.delete(winner)
        db.session.commit()
        return jsonify({"message": "Winner deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin_tickets', methods=['GET'])
def admin_tickets():
    ticket = Ticket.query.all()
    return jsonify([{

        'id' : u.id,
        'user_email': u.user_email,
        'lottery_id': u.lottery_id,
        'ticket_number': u.ticket_number,
        'timestamp' : u.timestamp
               # don't include password
    } for u in ticket]), 200




@app.route('/selected_winners', methods=['POST'])
def selected_winners():
    data = request.get_json()
    winners = data.get('approvedWinners', [])
    
    if not isinstance(winners, list):
        return jsonify({"error": "Invalid data format: 'SelectedWinner' should be a list."}), 400

    try:
        added_count = 0
        print(winners)
        for item in winners:
            name = item.get('userName') or item.get('name')
            # print(name)
            photo = item.get('userPhoto') or item.get('photo')

            amount = float(item.get('prize') or item.get('amount'))
            date = datetime.strptime(item.get('date'), "%Y-%m-%d").date()
            status = "Approved"
            contest_title = item.get('contestTitle')
            position = item.get('position')

            # Check if a winner with same name, contest, position, and date already exists
            # existing = Winner.query.filter_by(
            #     name=name,
            #     contestTitle=contest_title,
            #     position=position,
            #     date=date
            # ).first()

            # if existing:
            #     continue  # Skip duplicate
            
            if status == "Approved":
                
                new_winner = Winner.query.filter_by(name=name,contestTitle=contest_title).first()
                new_winner.status=status
                #     name=name,
                #     photo=photo,
                #     amount=amount,
                #     date=date,
                #     status=status,
                #     contestTitle=contest_title,
                #     position=positionBalance
                # )
                
                balance=Balance.query.filter_by(username=name).first()
                
                balance.balance+=amount
                
                db.session.add(new_winner)
                db.session.add(balance)
                added_count += 1
                db.session.commit()
                return jsonify({"message": f"{added_count} winner(s) addedd successfully!"}), 201

        db.session.commit()
        return jsonify({"message": "winner(s) not added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/result_img', methods=['POST'])
# @jwt_required()
def result_img():
    try:
        
        # print(query_date)
        result = Result.query.all()
        if result:
            return jsonify([{
                'id': u.id,
                'photo': u.image_url,
                'time' : u.date
                    
            } for u in result]), 200
        else:
            return jsonify({'photo' : None,'time' : None}), 404
    except:
        return jsonify({'error': 'Invalid request'}), 400

@app.route('/edit_result_img', methods=['POST'])
def edit_result_img():
    data = request.get_json()
    id = data.get('id')
    time = data.get('date')
    photo = data.get('photo')
    result = Result.query.filter_by(id=id).first()
    if not result :
        return jsonify({'error': 'result  not found'}), 404
    result.date=time
    result.image_url=photo  
    db.session.add(result)
    db.session.commit()
    return jsonify({'message': 'result changed'}), 200

@app.route('/add_result', methods=['POST'])
def add_result():
    data = request.get_json()
    try:
        result = Result(
            image_url=data.get('photo'),
            date = data.get('Date')
            
        )
        db.session.add(result)
        db.session.commit()
        return jsonify({"message": "Result added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/delete_result', methods=['POST'])
def delete_result():
    data = request.get_json()
    id = data.get('id')
    result = Result.query.filter_by(id=id).first()
    if not result:
        return jsonify({'error': 'result not found'}), 404
    db.session.delete(result)
    db.session.commit()
    return jsonify({'message': 'result deleted'}), 200 

@app.route("/qrcodes", methods=["GET"])
def get_qrcodes():
    qrs = QRCode.query.all()
    return jsonify([{
        "id": qr.id,
        "title": qr.title,
        "description": qr.description,
        "imageUrl": qr.image_url,
        "status": qr.status
    } for qr in qrs]), 200

@app.route("/add_qrcodes", methods=["POST"])
def add_qrcode():
    data = request.json
    new_qr = QRCode(
        title=data["title"],
        description=data.get("description", ""),
        image_url=data["imageUrl"],
        status=data.get("status", "Inactive")
    )
    db.session.add(new_qr)
    db.session.commit()
    return jsonify({
        "message":"completed"
    }), 200

@app.route("/edit_qrcodes", methods=["POST"])
def update_qrcode():
    data = request.get_json()
    id=data.get("id")
    qr = QRCode.query.filter_by(id=id).first()
    if not qr:
        return jsonify({"error": "QR code not found"}), 404

    data = request.json
    qr.title = data.get("title", qr.title)
    qr.description = data.get("description", qr.description)
    qr.image_url = data.get("imageUrl", qr.image_url)
    qr.status = data.get("status", qr.status)

    db.session.commit()
    return jsonify({
        "message":"completed"
    }), 200

@app.route("/delete_qrcodes", methods=["POST"])
def delete_qrcode():
    data = request.get_json()
    id=data.get("id")
    qr = QRCode.query.filter_by(id=id).first()
    if not qr:
        return jsonify({"error": "QR code not found"}), 404

    db.session.delete(qr)
    db.session.commit()
    return jsonify({"message": "QR code deleted"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
