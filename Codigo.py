import logging
import random
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


class Counter(object):
    def __init__(self):
        self.lock = threading.Lock()

    def increment(self):
        logging.debug('--> Intento acceder a la DB')
        self.lock.acquire()
        try:
            logging.debug('--> Accedio a la DB')
            pausa =2;
            logging.debug('--> durmiendo %0.02f',pausa)
            time.sleep(pausa)
        finally:
            self.lock.release()
            logging.debug('--> Dejo de usar la DB')

def worker(c):

        logging.debug('--> Creado correctamente')
        pausa = random.random()
        time.sleep(pausa)
        c.increment()


counter = Counter()

l1 = threading.Thread(name="Lector 1",target=worker, args=(counter,))
l2 = threading.Thread(name="Lector 2",target=worker, args=(counter,))
e1 = threading.Thread(name="Escritor 1",target=worker, args=(counter,))
e2 = threading.Thread(name="Escritor 2",target=worker, args=(counter,))
l1.start()
l2.start()
e1.start()
e2.start()

logging.debug('Esperando lectores/escritores"')
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()
