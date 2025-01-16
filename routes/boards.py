from flask import Blueprint, jsonify, request


boards_bp = Blueprint("boards", __name__)


# @boards_bp.route("/boards", methods=["GET"])
# def get_boards():
#     """Get all boards for the authenticated user"""
#     try:
#         boards = get_boards_for_user()
#         return jsonify(boards)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @boards_bp.route("/boards/<board_id>", methods=["GET"])
# def get_board(board_id):
#     """Get a specific board by ID"""
#     try:
#         board = get_boards_for_user(board_id)
#         if board is None:
#             return jsonify({"error": "Board not found"}), 404
#         return jsonify(board)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
