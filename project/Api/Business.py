from flask import jsonify, g, request
from flask_restful import Resource
import re
from project.models import Follow
from project.extra import login_required, checke_interface

class follow_interface(Resource):
    @login_required
    def get(self):
        re_com = re.compile(r'^action\=(\d)\&lastCursor\=\$(.*)$')
        r = re_com.match(request.query_string.decode('utf-8'))

        be_concerned_id = r.group(2)
        follow_operation = r.group(1)

        if follow_operation == '1' and \
            g.user.user_follow(be_concerned_id,follow_operation):
            return jsonify(status=1,
                            action_status=1,
                            message="关注成功")
        elif follow_operation == '0' and \
            g.user.user_follow(be_concerned_id, follow_operation):
                return jsonify(status=1,
                               action_status=1,
                               message="取消关注成功")
        else:
            return jsonify(status=0, message="failed")
