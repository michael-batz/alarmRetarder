#! /usr/bin/python3

import sched, time


def sendEvent(text):
	print(text)


eventScheduler = sched.scheduler(time.time, time.sleep)

eventScheduler.enter(10, 1, sendEvent, argument=('This is a testmessage 1', ))
eventScheduler.enter(5, 1, sendEvent, argument=('This is a testmessage 2', ))

eventScheduler.run()
