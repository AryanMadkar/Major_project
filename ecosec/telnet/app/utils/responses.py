from flask import jsonify

# ======================================================
# SUCCESS RESPONSE
# ======================================================

def success_response(message, data=None):

    return jsonify({

        "success": True,

        "message": message,

        "data": data
    })

# ======================================================
# ERROR RESPONSE
# ======================================================

def error_response(message, status=400):

    return jsonify({

        "success": False,

        "error": message
    }), status