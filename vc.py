"""
  CSC464 Assignment 2
  Vector Clocks in Python

  Thor Reite V00809409
  11/21/2018

"""

MAX_MESSAGES = 7
p = [[0, 0, 0], [0, 0, 0], [0, 0, 0]] #each element of p is a clock

def main():
    messages().run()

class messages():
    def run(self):
        num_messages = 0
        while num_messages < MAX_MESSAGES: #program ends after MAX_MESSAGES sends and receives
            sender = int(input("Specify sending process: ")) #user input
            receiver = int(input("Specify receiving process: ")) #user input
            if sender >= 0 and receiver >= 0 and sender < 3 and receiver < 3:
                if sender == receiver:
                    p[sender][receiver] +=1 #if sending to self only increase own clock
                else:
                    p[sender][sender] +=1 #increase sender clock
                    p[receiver][receiver] +=1 #increase receiver clock
                    for i in range(3):
                        if receiver is not i: #receiver retains its own clock
                            p[receiver][i] = max(p[receiver][i], p[sender][i]) #change receiver clock to max of sender/receiver
                print("Sender process %s now has clock [%s, %s, %s]" % (sender, p[sender][0], p[sender][1], p[sender][2]))
                print("Receiver process %s now has clock [%s, %s, %s]" % (receiver, p[receiver][0], p[receiver][1], p[receiver][2]))
                num_messages +=1 #program ends after MAX_MESSAGES sends and receives
            else:
                print("Please enter a number within range(3).")
        ##display clocks after all messages have been sent
        for i in range(3):
            print("Process %s has clock [%s, %s, %s]" % (i, p[i][0], p[i][1], p[i][2]))

if __name__ == '__main__':
    main()
