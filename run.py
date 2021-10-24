import datetime
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'iot'
app.config['MONGO_URI'] = 'mongodb://root:secret@localhost:27017/iotdb?authSource=admin'

mongo = PyMongo(app)

#db_operations = mongo.db.<COLLECTION_NAME>)
print("###################")
print(mongo.db)
# print(mongo.db.temp)
iot_db_oper = mongo.db.temp
fit_db_step=  mongo.db.steps
output = []
for s in iot_db_oper.find():
  print(s)

@app.route('/temp', methods=['GET'])
def get_temp_state():
    output = []
    for s in iot_db_oper.find():
        output.append(s)
    return jsonify({'result': output})

@app.route('/temp-latest', methods=['GET'])
def get_temp_st():
    output_cur = iot_db_oper.find().skip(iot_db_oper.count() - 1)
    res= next(output_cur,'None')
    return jsonify({'result': res})


@app.route('/temp-add', methods=['POST'])
def add_temp_state():
    print(request.json)
    dtime = request.json['datetime']
    temperature = request.json['temperature']
    temp_id = iot_db_oper.insert({'_id': "{}-{}".format(dtime, temperature), 'time': dtime, 'temperature': temperature})
    return jsonify({'result': temp_id})

@app.route('/steps-add', methods=['POST'])
def add_steps():
    dtime = request.json['datetime']
    steps = request.json['steps']
    stp_id = fit_db_step.insert({'_id': "{}-{}".format(dtime, steps), 'time': dtime, 'steps': steps})
    return jsonify({'result': stp_id})


@app.route('/steps-all', methods=['GET'])
def get_steps_all():
    output = []
    for s in fit_db_step.find():
        output.append(s)
    return jsonify({'result': output})


@app.route('/steps-current', methods=['GET'])
def get_steps():
    output_cur = fit_db_step.find().skip(fit_db_step.count() - 1)
    print(output_cur)
    res= next(output_cur,'0')
    return jsonify({'result': res})


@app.route('/step-reset', methods=['POST'])
def steps_reset():
    dtime = datetime.datetime.now().strftime('%Y:%m:%d-%H:%M:%S')
    stp_id = fit_db_step.insert({'_id': "{}-{}".format(dtime, 0), 'time': dtime, 'steps': '0'})
    return jsonify({'result': stp_id})

if __name__ == '__main__':
    print("hi")
    app.run(host='0.0.0.0', port=5001, debug=True)
