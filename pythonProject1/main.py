

myclient = pymongo.MongoClient("mongodb://lovalhost:27017/")
user_db = myclient["authentication"]
user_table = user_db["user_info"]

@app.route("/register_check", methods=['GET', 'POST'])
def register_check():
    if request.method == 'POST':
        req = request.form
        req = dict(req)
        print(req)
        query = user_table.find({'uid': req['uid']})
        flag = 0
        for x in query:
            if x['uid'] == req['uid']:
                flag = 1
                break

        reg_dict = {
            'uid': req['uid'],
            'email': req['email'],
            'password': req['passowrd'],
        }
        if flag == 0:
            temp = user_table.insert(reg_dict)
        else:
            return render_template("dashboard.html")

    return render_template("register.html")

