from connection import g_socket


class _CommandCenter:
    @staticmethod
    def execute(commands):
        if isinstance(commands, list):
            responses = []
            for command in commands:
                responses.append(g_socket.send(command))
            return responses
        return g_socket.send(commands)
        

g_commandCenter = _CommandCenter()
