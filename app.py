from flask import Flask, jsonify, redirect
from body.blockchain import Blockchain

# Web app creation
app = Flask(__name__)
app.config["SECRET_KEY"] = "test_key"

# Creates object of the class blockchain.
blockchain = Blockchain()


# Mining a new block
@app.route("/api/v1/blocks/mine", methods=["GET"])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)

    # Block building
    block = blockchain.create_block(proof, previous_hash)

    response = {"message": "A block is mined",
                "index": block["index"],
                "timestamp": block["timestamp"],
                "proof": block["proof"],
                "previous_hash": block["previous_hash"],
                }

    return jsonify(response), 200


# Displaying blockchain
@app.route("/api/v1/blocks", methods=["GET"])
def display_chain():
    response = {"chain": blockchain.chain,
                "len": len(blockchain.chain)}
    return jsonify(response), 200


# Validity checker
@app.route("/api/v1/blocks/validity", methods=["GET"])
def valid():
    validity = blockchain.chain_valid()

    if validity:
        response = {"message": "The blockchain is valid."}
    else:
        response = {"message": "The blockchain is invalid"}
    return jsonify(response), 200


# Default route. Redirects to the blockchain
@app.route("/", methods=["GET"])
def index():
    return redirect("/api/v1/blocks")


# Run flask server locally
app.run(host="127.0.0.1", port=5000)

"""
http://127.0.0.1:5000/api/v1/blocks - View chain,
http://127.0.0.1:5000/api/v1/blocks/validity - Chain validity,
http://127.0.0.1:5000/api/v1/blocks/mine - Block mining
"""