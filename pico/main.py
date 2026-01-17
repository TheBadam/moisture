from micro_logging import log_message
from sensor import read_sensor
from server import connect, open_socket, serve

if __name__ == "__main__":
    filename = "error.log"
    log_message(filename, "Power ON")
    conn = None
    try:
        ip = connect()
        conn = open_socket(ip)
        serve(conn, read_sensor)
    except Exception as e:
        print(e)
        log_message(filename, e)  
    finally:
        print("Exit")
        if conn is not None:
            conn.close()
        log_message(filename, "Exit")
        
        
