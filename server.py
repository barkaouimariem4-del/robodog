"""Serveur de commande du Robodog (Flask).
Lancer : python server.py  puis ouvrir http://IP_DE_LA_PI:5000
"""
import threading
import time
from flask import Flask, jsonify, request, send_from_directory

TIMEOUT = 0.4      # s : sans message du navigateur, le robot s'arrête
LOOP_HZ = 50       # fréquence de la boucle de marche

app = Flask(__name__)


class Robot:
    """Point de branchement avec ton code de marche (kinematics / gait)."""

    def __init__(self):
        self.vx = 0        # -1 reculer, 0 arrêt, 1 avancer
        self.turn = 0      # -1 droite, 0 aucun, 1 gauche
        self.last_seen = time.time()
        self.lock = threading.Lock()

    def set_command(self, vx, turn):
        with self.lock:
            self.vx, self.turn = vx, turn
            self.last_seen = time.time()

    def apply(self, vx, turn):
        # TODO : appeler ton générateur de marche ici.
        # Exemple : gait.step(forward=vx, rotation=turn)
        pass

    def loop(self):
        prev = None
        while True:
            with self.lock:
                if time.time() - self.last_seen > TIMEOUT:
                    self.vx, self.turn = 0, 0          # sécurité : arrêt
                cmd = (self.vx, self.turn)
            if cmd != prev:
                print(f"commande : avance={cmd[0]:+d} rotation={cmd[1]:+d}")
                prev = cmd
            self.apply(*cmd)
            time.sleep(1 / LOOP_HZ)


robot = Robot()
threading.Thread(target=robot.loop, daemon=True).start()


def clamp(v):
    return max(-1, min(1, int(v)))


@app.post("/cmd")
def cmd():
    data = request.get_json(silent=True) or {}
    robot.set_command(clamp(data.get("vx", 0)), clamp(data.get("turn", 0)))
    return jsonify(ok=True)


@app.get("/")
def index():
    return send_from_directory(".", "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
