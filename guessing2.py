print "Hi What's your name?"
name = raw_input()
print "Hi %r. Enter a number between 1 and 100" % name

import random

randomnum = random.randrange(1,101,1)
print randomnum

guess = int(raw_input())

while guess != randomnum:
	if guess < randomnum:
		print "too low"
		guess = int(raw_input())
	else:
		print "too high"
		guess = int(raw_input())

print "you got it"