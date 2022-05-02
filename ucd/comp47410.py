import os
from flask import Blueprint, current_app, jsonify, request, send_file
from CA4106.endpoints.ucd.cryptopunked import get_tweet

bp = Blueprint('comp47410', __name__, url_prefix="/ucd/comp47410")

@bp.route('/generate_tweet', methods=['POST'])
def generate_tweet():
  tweet = get_tweet(current_app)

  return jsonify(tweet=tweet), 201