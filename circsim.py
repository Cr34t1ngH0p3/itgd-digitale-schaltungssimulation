# concrete subject
class Wire:
  counter = 0

  # constructor
  # Wire() : state(0), id(++counter) {}
  def __init__(self):
    self.state = 0
    self.gates = []

    Wire.counter += 1
    self.id = Wire.counter

  # attaching wires
  # void reg(Gate* g)
  def reg(self, gate):
    self.gates.append(gate)

  # calls update for all gates
  def notify(self):
    for gate in self.gates:
      gate.update()

  # set new state
  # void operator()(bool p)
  def set(self, p):
    if p != self.state:
      self.state = p
      self.notify()

  def get(self):
    return self.state


class AND:
  counter = 0

  def __init__(self, _out, _in1, _in2):
    self.out = _out
    self.in1 = _in1
    self.in2 = _in2
    AND.counter += 1
    self.id = AND.counter
    self.in1.reg(self)
    self.in2.reg(self)
    self.update()

  def update(self):
    #print('debug', self.in1.get(), self.in2.get())
    self.out.set( self.in1.get() and self.in2.get() )


class NAND:
  counter = 0

  def __init__(self, _out, _in1, _in2):
    self.out = _out
    self.in1 = _in1
    self.in2 = _in2
    AND.counter += 1
    self.id = NAND.counter
    self.in1.reg(self)
    self.in2.reg(self)
    self.update()

  def update(self):
    #print('debug', self.in1.get(), self.in2.get())
    self.out.set( not(self.in1.get() and self.in2.get()) )


def main():
  w1 = Wire()
  w2 = Wire()
  w3 = Wire()

  AND(w3, w2, w1)

  print('w1', 'w2', 'w3')
  for k in range(2):
    for i in range(2):
      w1.set(k)
      w2.set(i)
      print(w1.get(), w2.get(), w3.get())



if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = GUI()
  window.show()

  sys.exit(app.exec_())

