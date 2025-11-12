from onboard_software.server import Server
import queue
        
class Robot:
    def __init__(self):

        self.server = Server()
        self.server.start()

        data = self.server.cmd_input_queue.get()
        if data == "TELEOP START":
            self.teleop_ctrl.start()
            self.mode = "TELEOP"
        elif data == "AUTONOMOUS START":
            self.auto_ctrl.start()
            self.mode = "AUTO"


    def toggle_mode(self, data):
        if self.mode == "AUTO" and data == "SWITCH TO TELEOP":
            print("[SUPERVISOR] Switching to TELEOP")
            self.auto_ctrl.stop()
            self.teleop_ctrl.start()
            self.mode = "TELEOP"
        elif self.mode == "TELEOP" and data == "SWITCH TO AUTONOMOUS":
            print("[SUPERVISOR] Switching to AUTO")
            self.teleop_ctrl.stop()
            self.auto_ctrl.start()
            self.mode = "AUTO"

    def run(self):
        
        try:
            while True:
                try:
                    data = self.server.cmd_input_queue.get_nowait()
                except queue.Empty:
                    data = None

                self.toggle_mode(data)
                cmd = data
                id = cmd[0]

        except KeyboardInterrupt:
            print("\n[CLIENT] Interrupted by user.")
        finally:
            print("[CLIENT] Shutting down.")
            
if __name__ == "__main__":
    Robot().run()
