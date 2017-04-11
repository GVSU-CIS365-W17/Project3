from multiprocessing import Process, Queue
import krpc

def f(q):
    krpc.connect(name="Test")
    q.put(True)

if __name__ == "__main__":
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    p.join(20)
    print("joining in 20")
    if p.is_alive():
        print("still alive")
        p.terminate()
    else:
        print("dead")
        print(q.get())