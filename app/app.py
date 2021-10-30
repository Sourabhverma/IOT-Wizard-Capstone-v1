import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

application = Flask(__name__)
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGO_INITDB_ROOT_USERNAME'] + ':' + os.environ[
    'MONGO_INITDB_ROOT_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ[
                                      'MONGODB_DATABASE'] + '?authSource=admin'

# application.config['MONGO_URI'] = 'mongodb://root:secret@127.0.0.1:27017/iotdb?authSource=admin'

mongo = PyMongo(application)
print("#########  Flask Server Started ##########")
print(mongo.db)

#db_operations = mongo.db.<COLLECTION_NAME>
dumpbin_db= mongo.db.dumpbins

@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Smart Garbage Management System!'
    )

@application.route('/bin-lat', methods=['GET'])
def get_bin_lat_updated():
    output_cur = dumpbin_db.find().skip(dumpbin_db.count() - 1)
    res = next(output_cur, '0')
    res.update({"_id": str(res.get("_id"))})
    return jsonify({'result': res})


@application.route('/bins-all', methods=['GET'])
def get_bins_all():
    output = []
    for s in dumpbin_db.find():
        s.update({"_id": str(s.get("_id"))})
        output.append(s)
    return jsonify({'result': output})


@application.route('/set-bin-status', methods=['POST'])
def insert_bin_status():
    bin_id = request.json['bin_id']
    ctime = request.json['datetime']
    status = request.json['status']
    region = request.json['region']
    geolocation = request.json['gelocation']
    upd_id = dumpbin_db.insert_one(
        {'_id': "{}-{}".format(bin_id, ctime), 'bin_id': bin_id, 'status': status, 'geolocation': geolocation,
         'region': region})
    return jsonify({'result': upd_id.inserted_id if upd_id.acknowledged else False})


@application.route('/bins-alert', methods=['GET'])
def get_all_bins_alert():
    region = request.args.get('region')
    status = request.args.get('status')
    count_row = (dumpbin_db.count() - 1) if dumpbin_db.count() > 0 else False
    if not count_row:
        print("No Dumpbins status updated and tracked")
        return jsonify({'result': "No Dumpbins status updated and tracked"})
    elif (status and region)and not dumpbin_db.find({'region': region, 'status': status}).count():
        print("For region {} No Dumpbins is {}".format(region,status))
        return jsonify({'result': "For region {} No Dumpbins is {}".format(region,status)})
    elif status and region:
        result_cur = dumpbin_db.find({'region': region, 'status': status})
        result=[]
        if result_cur:
            for row in result_cur:
                row.update({"_id": str(row.get("_id"))})
                result.append(row)
        return jsonify({'result': result if result else None})
    elif status and not region:
        result_cur = dumpbin_db.find({'status': status})
        result = []
        if result_cur:
            for row in result_cur:
                row.update({"_id": str(row.get("_id"))})
                result.append(row)
        return jsonify({'result': result if result else None})
    elif not status and region:
        result_cur = dumpbin_db.find({'region': region})
        result = []
        if result_cur:
            for row in result_cur:
                row.update({"_id": str(row.get("_id"))})
                result.append(row)
        return jsonify({'result': result if result else None})
    else:
        print("Please pass valid region or status")
        return jsonify({'result': "Please pass valid region or status"})

@application.route('/reset-bin-status', methods=['PUT'])
def update_bin_status():
    bin_id = str(request.json['bin_id'])
    region = request.json['region']
    upd_id = dumpbin_db.update_one({'bin_id': bin_id,'region' : region}, {'$set': {'status': 'empty'}})
    return jsonify({'result': {'modified_count': upd_id.modified_count,
                               'matched_count': upd_id.matched_count} if upd_id.acknowledged else False})


if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
