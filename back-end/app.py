import time

from flask import Flask, jsonify, request, make_response

from get_info import *
from translate import trans
from flask_cors import CORS
from translator import transl

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

app = Flask(__name__)

# 메인 페이지(홈 페이지) 라우팅/ 리퀘스트 방법 GET, POST
@app.route("/translation/food", methods=['POST', 'OPTIONS'])
def traslation():
    if request.method == 'OPTIONS': 
        return build_preflight_response()
    lan_type = request.args.get('data')

    data = get_food()
    building = []
    restaurant = []
    food_list = ["효민 기숙사", "행복 기숙사", "정보공학관", "수덕전"]

    for key in data:
        building.append([key, data[key]])

    # hyomin      = building[0]
    # happy       = building[1]
    # inforamtion  = building[2]
    # suduck      = building[3]

    if building[0][1][0]['Date'] == 'No data':
        building[0] = ['hyomin', None]
    if building[2][1] == None:
        building[2] = ['inforamtion', None]
    if building[3][1] == None:
        building[3] = ['suduck', None]

    for day in building:
        if day[1] is not None:
            for data in day[1]:
                if data['Date'] == time.strftime("%Y-%m-%d", time.localtime(time.time())):
                    breakfast = data['breakfast']
                    lunch = data['lunch_s']
                    dinner = data['dinner']
                    if lan_type != 'ko':
                        breakfast = trans(breakfast, lan_type)
                        lunch = trans(lunch, lan_type)
                        dinner = trans(dinner, lan_type)
                    break
        else:
            breakfast = None
            lunch = None
            dinner = None

        food_list.append([breakfast, lunch, dinner])

    restaurant.append(food_list)

    return build_actual_response(jsonify({"restaurant":restaurant}))

@app.route("/building/info", methods=['POST', 'OPTIONS'])
def information():

    build_info = []

    if request.method == 'OPTIONS': 
        return build_preflight_response()
    elif request.method == "POST":
        keyword = request.args.get('keyword')
        lan_type = request.args.get('lan_type')

        if lan_type == "ko":
            build_info = school_info(keyword)
        else :
            build_info = school_info(keyword)
            for i in range(len(build_info)):
                tr = trans(build_info[i][1], lan_type)
                build_info[i][1] = tr
    return build_actual_response(jsonify({"build_info":build_info}))

@app.route("/translator",  methods=['POST', 'OPTIONS'])
def translator():
    if request.method == 'OPTIONS': 
        return build_preflight_response()
    txt = request.args.get('text')
    lan_type = request.args.get('lan_type')

    return_txt = transl(txt, lan_type)

    return build_actual_response(jsonify({"return_txt":return_txt}))

@app.route("/calender", methods=['POST', 'OPTIONS'])
def calen():
    if request.method == 'OPTIONS': 
        return build_preflight_response()
    lan_type = request.args.get('lan_type')

    calen_list = date_info()

    if lan_type == "ko":
        return build_actual_response(jsonify({"calen_list":calen_list}))
    else:
        total_list = []
        for i in range(len(calen_list)):
            semi_list = []
            for j in range(len(calen_list[i])):
                date = trans(calen_list[i][j], lan_type)
                semi_list.append(date)
            total_list.append(semi_list)
        return build_actual_response(jsonify({"total_list":total_list}))



# debug 모드로 실행
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)