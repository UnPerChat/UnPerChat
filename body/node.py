import rsa
import os


class Node:
    def __init__(self):
        if os.path.isfile("private.pem") and os.path.isfile("public.pem"):
            self.pubkey, self.privkey = self.key_loader()
        else:
            self.pubkey, self.privkey = self.key_generator()
            self.key_saver()
        self.node_id = self.pubkey.save_pkcs1().decode('utf-8')
        self.known_nodes = set()
        self.trusted_nodes = set()
        self.banned_nodes = set()

    def key_generator(self):
        return rsa.newkeys(512)

    def get_node_id(self):
        return self.node_id

    def key_saver(self):
        with open("private.pem", "wb") as f:
            f.write(self.privkey.save_pkcs1())
        with open("public.pem", "wb") as f:
            f.write(self.pubkey.save_pkcs1())

    def key_loader(self):
        with open("private.pem", "rb") as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read())
        with open("public.pem", "rb") as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read())
        return pubkey, privkey

    def add_known_node(self, node_id):
        self.known_nodes.add(node_id)

    def remove_known_node(self, node_id):
        if node_id in self.known_nodes:
            self.known_nodes.remove(node_id)

    def add_trusted_node(self, node_id):
        if node_id not in self.known_nodes:
            raise Exception("Can not trust unknown node!")
        self.trusted_nodes.add(node_id)

    def remove_trusted_node(self, node_id):
        if node_id in self.trusted_nodes:
            self.trusted_nodes.remove(node_id)

    def ban_node(self, node_id):
        if node_id in self.known_nodes:
            self.remove_known_node(node_id)
        if node_id in self.trusted_nodes:
            self.remove_trusted_node(node_id)
        self.banned_nodes.add(node_id)
