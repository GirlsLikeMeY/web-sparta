from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def write_review():
    # 1. 클라이언트가 준 title, author, review 가져오기.
    title_receive = request.form.get('title_give')
    author_receive = request.form.get('author_give')
    review_receive = request.form.get('review_give')

    doc = {
        "title": title_receive,
        "author": author_receive,
        "review": review_receive

    }
    print(doc)
    # 2. DB에 정보 삽입하기
    db.reviews.insert_one(doc)
    # 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '리뷰 작성완료!'})


# 겟 방식은 브라우저에서 확인 가능함

@app.route('/review', methods=['GET'])
def read_reviews():
    # 모든 데이터 불러오기(find)
    #_id : false 라는 것은 여기 데이터는 가져오지 않겠다는 것

    # 이거 data list 처리 안해줘서 오류 났었음ㅠㅠ 더 공부해야겠다 진짜....
    data = list(db.reviews.find({}, {"_id": False}))
    print(data)
    return jsonify({'result': 'success', 'data': data})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

